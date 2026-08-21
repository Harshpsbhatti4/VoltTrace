# VoltTrace
> **Edge-Powered Smart Plug Platform with Embedded Physical AI**  
> *Developed for the Arduino Physical AI Challenge India 2026*

---

## Abstract
**VoltTrace** is an intelligent, edge-controlled smart energy monitoring and safety plug platform. By deploying physical AI directly onto the Arduino platform, VoltTrace samples and processes electrical signatures (voltage, current, active power, power factor, and crest factor) entirely on-device. 

The system leverages a dual-core processing architecture where raw 10-bit analog electrical sampling on the microcontroller (MCU) core streams seamlessly via Inter-Process Communication (IPC) over the Arduino RouterBridge into a Linux MPU core. Running an on-board Machine Learning pipeline (Random Forest NILM Classifier & Autoencoders), VoltTrace provides real-time Non-Intrusive Load Monitoring (NILM) fingerprinting, dynamic Universal Health Scoring ($0\% - 100\%$), early fault prediction, and autonomous hardware relay protection without cloud latency.

---

## Key Features
* **Edge Physical AI Inference:** Real-time on-device classification and anomaly detection using scikit-learn Random Forests and load-specific Autoencoders.
* **Dual-Core IPC Processing:** MCU core handles high-speed analog sampling ($192\text{ samples/cycle}$), zero-bias clamping, and RMS/Power Factor math before streaming telemetry to the Python MPU backend.
* **Autonomous Circuit Protection:** Instantaneous fault detection and automatic relay cut-off on GPIO Pin 7 for overcurrent, short circuits, thermal runaway, and mains voltage anomalies.
* **Hysteresis & Load Lock Retention:** Noise-gated signal processing prevents low-power adapter micro-fluctuations from causing UI false positives or state resets.
* **Local Web Dashboard & Cloud Sync:** Embedded FastAPI web server hosted on port `7000` provides interactive real-time telemetry analytics accessible from any network device.

---

## System Architecture

```text
+------------------------------------+        +-----------------------------------+
|       Arduino MCU Core (C++)       |        |       Linux MPU Core (Python)     |
| - 10-bit A1/A2 Signal Sampling     |  IPC   | - Random Forest NILM Classifier   |
| - RMS V/I, Power, PF, Crest Factor | -----> | - Autoencoder Anomaly Diagnostics |
| - Pin 7 Relay Control Actuation    | Bridge | - Local FastAPI Server (Port 7000)|
+------------------------------------+        +-----------------------------------+
