import os
import sys
import json
import time
import threading
import joblib
import numpy as np
import sklearn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn

from arduino.app_utils import App, Bridge

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

def resolve_file(filename):
    root_path = os.path.join(ROOT_DIR, filename)
    local_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(root_path):
        return root_path
    if os.path.exists(local_path):
        return local_path
    return root_path

try:
    scaler_nilm = joblib.load(resolve_file("scaler_nilm.joblib"))
    model_nilm = joblib.load(resolve_file("model_nilm_rf.joblib"))
    class_names = joblib.load(resolve_file("class_names.joblib"))
    autoencoders = joblib.load(resolve_file("models_autoencoders.joblib"))
    scalers_ae = joblib.load(resolve_file("scalers_ae.joblib"))
    print("[+] ML Models loaded successfully.")
except Exception as e:
    print(f"[!] Warning: Model load failed ({e})")
    scaler_nilm = model_nilm = class_names = autoencoders = scalers_ae = None

ema_v = 230.0
ema_i = 0.0
ema_p = 0.0
ema_pf = 1.0
ema_cf = 1.414
locked_appliance_name = None
last_active_appliance = None

def run_ml_diagnostics(v_raw, i_raw, p_raw, pf_raw, cf_raw, temp_c):
    global ema_v, ema_i, ema_p, ema_pf, ema_cf, locked_appliance_name, last_active_appliance

    ema_v = 0.35 * v_raw + 0.65 * ema_v
    
    if i_raw >= 0.04:
        ema_i = 0.35 * i_raw + 0.65 * ema_i
        ema_p = 0.35 * p_raw + 0.65 * ema_p
        ema_pf = 0.35 * pf_raw + 0.65 * ema_pf
        ema_cf = 0.35 * cf_raw + 0.65 * ema_cf

    if ema_i < 0.04 and last_active_appliance is None and locked_appliance_name is None:
        return {
            "health_pct": 100.0,
            "classification": "NO LOAD DETECTED",
            "appliance": "No Load Connected",
            "load_type": "Standby",
            "reasons": [],
            "v_norm": round(v_raw / 230.0, 2),
            "i_norm": 0.0,
        }

    features = np.array([[ema_v, ema_i, ema_p, ema_pf, ema_cf]])

    if locked_appliance_name and locked_appliance_name != "No Load Connected":
        detected_class = locked_appliance_name
    elif last_active_appliance and last_active_appliance != "No Load Connected":
        detected_class = last_active_appliance
    elif model_nilm is not None and scaler_nilm is not None and ema_i >= 0.04:
        feats_scaled = scaler_nilm.transform(features)
        pred_idx = model_nilm.predict(feats_scaled)[0]
        detected_class = class_names[pred_idx]
        last_active_appliance = detected_class
    else:
        if ema_cf > 2.0 or ema_pf < 0.70:
            detected_class = "LED Lighting / SMPS"
        elif ema_pf > 0.90:
            detected_class = "Incandescent Bulb (100W/200W)" if ema_p > 90 else "Soldering Iron / Heating Element"
        else:
            detected_class = "Inductive Fan / Desk Motor"
        last_active_appliance = detected_class

    if "SMPS" in detected_class or "LED" in detected_class or "Laptop" in detected_class or "Phone" in detected_class:
        load_type = "Capacitive / Non-Linear"
        p_ref, pf_ref, cf_ref, i_trip_limit = 50.0, 0.65, 3.50, 2.50
    elif "Incandescent" in detected_class:
        load_type = "Resistive (Thermal)"
        p_ref, pf_ref, cf_ref, i_trip_limit = 185.0, 0.99, 1.414, 1.40
    elif "Soldering" in detected_class or "Heating" in detected_class:
        load_type = "Resistive (Thermal)"
        p_ref, pf_ref, cf_ref, i_trip_limit = 60.0, 0.99, 1.414, 1.40
    else:
        load_type = "Inductive (Motor)"
        p_ref, pf_ref, cf_ref, i_trip_limit = 60.0, 0.78, 1.60, 1.50

    i_ref = p_ref / (230.0 * pf_ref)
    v_norm = ema_v / 230.0
    i_norm = ema_i / i_ref

    ae_health = 96.0
    if autoencoders and scalers_ae and detected_class in autoencoders:
        try:
            ae_meta = autoencoders[detected_class]
            scaler = scalers_ae[detected_class]
            x_ae = scaler.transform(features)
            recon = ae_meta["model"].predict(x_ae)
            mse = float(np.mean((x_ae - recon) ** 2))
            z_score = max(0.0, (mse - ae_meta["mse_mean"]) / (5.0 * ae_meta["mse_std"] + 1e-6))
            ae_health = float(np.clip(100.0 / (1.0 + 0.15 * (z_score ** 1.8)), 10.0, 100.0))
        except Exception:
            ae_health = 95.0

    reasons = []
    critical = False
    flag = False

    if i_norm > i_trip_limit:
        flag = critical = True
        reasons.append("OVERCURRENT_OR_SHORT_CIRCUIT")
    if temp_c > 85.0:
        flag = critical = True
        reasons.append("THERMAL_RUNAWAY")
    
    if v_norm < 0.74 or v_norm > 1.24:
        flag = True
        reasons.append("MAINS_VOLTAGE_OUT_OF_BAND")
        
    if ema_pf < 0.08 and ema_i > 0.40:
        flag = True
        reasons.append("SEVERE_POWER_FACTOR_DEGRADATION")

    if critical:
        health_score = min(ae_health, 10.0)
    elif flag:
        health_score = min(ae_health, 60.0)
    else:
        health_score = ae_health

    if health_score >= 80.0:
        classification = "OPTIMAL HEALTH"
    elif health_score >= 50.0:
        classification = "DEGRADED STATE"
    else:
        classification = "CRITICAL FAULT"

    return {
        "health_pct": round(health_score, 1),
        "classification": classification,
        "appliance": detected_class,
        "load_type": load_type,
        "reasons": reasons,
        "v_norm": round(v_norm, 3),
        "i_norm": round(i_norm, 3),
    }

latest_telemetry = {
    "timestamp": "", "v_rms": 0.0, "i_rms": 0.0, "power": 0.0, "temp": 28.5,
    "v_norm": 0.0, "i_norm": 0.0, "power_factor": 1.0, "crest_factor": 1.414,
    "health_score": 100.0, "classification": "STANDBY",
    "detected_appliance": "Detecting...", "detected_type": "Detecting...",
    "status": "Connected"
}

app_server = FastAPI()
app_server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app_server.get("/")
def serve_index():
    index_path = resolve_file("index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>VoltTrace Engine Active</h1>")

@app_server.get("/api/telemetry")
def get_telemetry():
    return latest_telemetry

@app_server.post("/api/lock-fingerprint")
def lock_fingerprint():
    global locked_appliance_name
    locked_appliance_name = latest_telemetry["detected_appliance"]
    return {"status": "locked", "appliance": locked_appliance_name}

@app_server.post("/api/reset-fingerprint")
def reset_fingerprint():
    global locked_appliance_name, last_active_appliance, ema_i, ema_p
    locked_appliance_name = None
    last_active_appliance = None
    ema_i = 0.0
    ema_p = 0.0
    return {"status": "unlocked"}

def start_web_server():
    uvicorn.run(app_server, host="0.0.0.0", port=7000, log_level="warning")

threading.Thread(target=start_web_server, daemon=True).start()

def record_telemetry(v_rms, i_rms, p_act, pf, crest_factor, temperature):
    global latest_telemetry
    try:
        v = float(v_rms)
        i = float(i_rms)
        p = float(p_act)
        pf_val = float(pf)
        cf = float(crest_factor)
        t = float(temperature)

        diag = run_ml_diagnostics(v, i, p, pf_val, cf, t)

        latest_telemetry.update({
            "timestamp": time.strftime("%H:%M:%S"),
            "v_rms": round(v, 1),
            "i_rms": round(ema_i, 3),
            "power": round(ema_p, 1),
            "temp": round(t, 1),
            "v_norm": diag["v_norm"],
            "i_norm": diag["i_norm"],
            "power_factor": round(ema_pf, 2),
            "crest_factor": round(ema_cf, 2),
            "health_score": diag["health_pct"],
            "classification": diag["classification"],
            "detected_appliance": diag["appliance"],
            "detected_type": diag["load_type"],
            "status": "Connected",
        })
    except Exception as e:
        print(f"[!] Processing error: {e}")

Bridge.provide("record_telemetry", record_telemetry)

App.run()
