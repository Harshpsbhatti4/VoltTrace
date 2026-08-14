# VoltTrace Physical AI Models

This directory contains the machine learning models, quantization workflows, and embedded C++ header files used for on-device electrical anomaly detection and load classification.

---

## Model Architecture & Overview

* **Task:** Real-Time Electrical Signature Classification & Anomaly Detection
* **Framework:** TensorFlow / Keras converted via TensorFlow Lite Micro (TFLM)
* **Target Hardware:** Arduino UNO Q / 32-bit Microcontroller
* **Inference Latency:** < 5 ms per inference cycle
* **Quantization:** Fully integer-quantized (`INT8`) weights and activations

---

## Feature Vector Structure
The model takes a normalized 6-dimensional feature vector extracted by `DSPProcessor`:

| Feature Index | Parameter | Description |
| :--- | :--- | :--- |
| `0` | $V_{\text{RMS}}$ | Normalized RMS Voltage |
| `1` | $I_{\text{RMS}}$ | Normalized RMS Current |
| `2` | $P_{\text{active}}$ | Active Power (Watts) |
| `3` | $PF$ | Power Factor ($\cos \theta$) |
| `4` | $CF$ | Current Crest Factor ($I_{\text{peak}} / I_{\text{RMS}}$) |
| `5` | $THD_{\text{est}}$ | Estimated Total Harmonic Distortion / Form Factor |

---

## File Structure

```text
models/
├── model.tflite        # Quantized INT8 TensorFlow Lite model
├── model_data.h        # C-byte array generated via xxd for microcontroller inclusion
├── train_model.py      # Offline Python script for dataset training and quantization
└── README.md           # Model specifications and usage guide
