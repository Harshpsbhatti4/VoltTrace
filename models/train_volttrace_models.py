import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

APPLIANCE_CLASSES = [
    {"name": "LED Lighting / SMPS", "v_mean": 235.0, "v_std": 6.0, "i_mean": 0.15, "i_std": 0.03, "p_mean": 22.0, "p_std": 4.0, "pf_mean": 0.62, "pf_std": 0.05, "cf_mean": 3.10, "cf_std": 0.25},
    {"name": "Incandescent Bulb (100W/200W)", "v_mean": 238.0, "v_std": 6.0, "i_mean": 0.81, "i_std": 0.04, "p_mean": 185.0, "p_std": 12.0, "pf_mean": 0.99, "pf_std": 0.01, "cf_mean": 1.414, "cf_std": 0.03},
    {"name": "Soldering Iron / Heating Element", "v_mean": 235.0, "v_std": 5.0, "i_mean": 0.26, "i_std": 0.03, "p_mean": 60.0, "p_std": 5.0, "pf_mean": 0.99, "pf_std": 0.01, "cf_mean": 1.414, "cf_std": 0.03},
    {"name": "Inductive Fan / Desk Motor", "v_mean": 235.0, "v_std": 6.0, "i_mean": 0.32, "i_std": 0.04, "p_mean": 58.0, "p_std": 8.0, "pf_mean": 0.76, "pf_std": 0.04, "cf_mean": 1.62, "cf_std": 0.08},
    {"name": "Laptop Charger / Adapter", "v_mean": 235.0, "v_std": 6.0, "i_mean": 0.38, "i_std": 0.06, "p_mean": 52.0, "p_std": 10.0, "pf_mean": 0.58, "pf_std": 0.06, "cf_mean": 2.85, "cf_std": 0.20},
    {"name": "Hair Dryer (Thermal High)", "v_mean": 232.0, "v_std": 7.0, "i_mean": 5.20, "i_std": 0.30, "p_mean": 1200.0, "p_std": 60.0, "pf_mean": 0.99, "pf_std": 0.01, "cf_mean": 1.414, "cf_std": 0.03},
    {"name": "Microwave Oven", "v_mean": 232.0, "v_std": 7.0, "i_mean": 4.50, "i_std": 0.35, "p_mean": 950.0, "p_std": 50.0, "pf_mean": 0.91, "pf_std": 0.03, "cf_mean": 1.75, "cf_std": 0.10},
    {"name": "Vacuum Cleaner", "v_mean": 232.0, "v_std": 7.0, "i_mean": 3.80, "i_std": 0.25, "p_mean": 820.0, "p_std": 45.0, "pf_mean": 0.93, "pf_std": 0.02, "cf_mean": 1.55, "cf_std": 0.08},
]

def generate_dataset(samples_per_class=400):
    np.random.seed(42)
    features, labels = [], []
    class_names = [item["name"] for item in APPLIANCE_CLASSES]

    for idx, item in enumerate(APPLIANCE_CLASSES):
        v = np.random.normal(item["v_mean"], item["v_std"], samples_per_class)
        i = np.random.normal(item["i_mean"], item["i_std"], samples_per_class)
        p = np.random.normal(item["p_mean"], item["p_std"], samples_per_class)
        pf = np.clip(np.random.normal(item["pf_mean"], item["pf_std"], samples_per_class), 0.1, 1.0)
        cf = np.clip(np.random.normal(item["cf_mean"], item["cf_std"], samples_per_class), 1.1, 4.5)

        features.append(np.column_stack([v, i, p, pf, cf]))
        labels.extend([idx] * samples_per_class)

    return np.vstack(features), np.array(labels), class_names

def train_and_export():
    X, y, class_names = generate_dataset()
    scaler_nilm = StandardScaler()
    X_scaled = scaler_nilm.fit_transform(X)

    nilm_rf = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    nilm_rf.fit(X_scaled, y)

    joblib.dump(scaler_nilm, "scaler_nilm.joblib")
    joblib.dump(nilm_rf, "model_nilm_rf.joblib")
    joblib.dump(class_names, "class_names.joblib")

    autoencoders, scalers_ae = {}, {}
    for idx, name in enumerate(class_names):
        X_cls = X[y == idx]
        scaler_ae = StandardScaler()
        X_cls_scaled = scaler_ae.fit_transform(X_cls)

        ae = MLPRegressor(hidden_layer_sizes=(3,), activation="tanh", solver="lbfgs", max_iter=1000, random_state=42)
        ae.fit(X_cls_scaled, X_cls_scaled)

        recon = ae.predict(X_cls_scaled)
        mse = np.mean((X_cls_scaled - recon) ** 2, axis=1)

        autoencoders[name] = {"model": ae, "mse_mean": float(mse.mean()), "mse_std": float(max(mse.std(), 1e-6))}
        scalers_ae[name] = scaler_ae

    joblib.dump(autoencoders, "models_autoencoders.joblib")
    joblib.dump(scalers_ae, "scalers_ae.joblib")
    print("[✓] Model artifacts successfully compiled!")

if __name__ == "__main__":
    train_and_export()