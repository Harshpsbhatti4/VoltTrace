```markdown
# VoltTrace | Machine Learning & Diagnostic Pipeline

The Linux MPU core executes a dual-stage machine learning engine combining **Non-Intrusive Load Monitoring (NILM)** classification with **Autoencoder-based Anomaly Detection**.

---

## 1. Feature Vector Representation

Every $250\text{ms}$ interval, the MPU builds a 5-dimensional feature vector derived from Exponential Moving Average (EMA) smoothed telemetry:

$$\mathbf{X} = \begin{bmatrix} V_{EMA} & I_{EMA} & P_{EMA} & PF_{EMA} & CF_{EMA} \end{bmatrix}$$

---

## 2. Stage 1: Random Forest NILM Classifier

A trained **Random Forest Classifier** (`model_nilm_rf.joblib`) analyzes electrical signatures to identify connected appliances:

* **Resistive Loads** ($PF \approx 0.99, CF \approx 1.41$): Incandescent Bulbs, Heaters, Soldering Irons.
* **Inductive Loads** ($PF < 0.85, CF \approx 1.5-1.8$): Electric Motors, Fans, Pumps.
* **Capacitive / Non-Linear SMPS** ($PF < 0.70, CF > 2.5$): LED Bulbs, Laptop Power Bricks, Mobile Chargers.

---

## 3. Stage 2: Autoencoder Anomaly & Health Scoring

1. **Reconstruction Loss**: The feature vector is passed to a load-specific Autoencoder (`models_autoencoders.joblib`).
2. **Mean Squared Error (MSE)**: The model measures deviation between input feature $\mathbf{X}$ and reconstructed output $\mathbf{\hat{X}}$:
   $$MSE = \frac{1}{n} \sum_{i=1}^{n} (X_i - \hat{X}_i)^2$$
3. **Health Score Mapping**: The $Z$-score of the MSE maps dynamically to a $0\% - 100\%$ Universal Health Score:
   $$\text{Health \%} = \text{clip}\left(\frac{100}{1 + 0.15 \cdot Z^{1.8}}, 10.0, 100.0\right)$$
