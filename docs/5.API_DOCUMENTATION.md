# VoltTrace | REST API Documentation

The MPU runs a local **FastAPI** web server on port `7000` to serve dashboard UI requests, stream telemetry, and allow remote control of fingerprint locks.

---

## Endpoints Summary

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Serves the main `index.html` web dashboard interface. |
| `/api/telemetry` | `GET` | Returns real-time electrical metrics and AI diagnostic results. |
| `/api/lock-fingerprint` | `POST` | Locks the current detected load fingerprint for the test run. |
| `/api/reset-fingerprint` | `POST` | Unlocks load classification and resets current/power EMAs to standby. |

---

## Detailed Endpoint Specifications

### 1. Get Real-Time Telemetry
* **URL**: `/api/telemetry`
* **Method**: `GET`
* **Response**: `200 OK`
* **Payload Structure**:
```json
{
  "timestamp": "18:05:22",
  "v_rms": 228.4,
  "i_rms": 0.412,
  "power": 94.1,
  "temp": 28.5,
  "v_norm": 0.993,
  "i_norm": 0.923,
  "power_factor": 0.99,
  "crest_factor": 1.41,
  "health_score": 100.0,
  "classification": "OPTIMAL HEALTH",
  "detected_appliance": "Incandescent Bulb (100W/200W)",
  "detected_type": "Resistive (Thermal)",
  "status": "Connected"
}
