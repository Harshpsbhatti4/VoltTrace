# VoltTrace ⚡
> **Edge-Powered Smart Plug Platform with Embedded Physical AI**  
> *Developed for the Arduino Physical AI Challenge India 2026*

---

## 📌 Abstract
**VoltTrace** is an intelligent, edge-controlled smart energy monitoring and safety plug platform. By deploying physical AI directly onto the microcontroller, VoltTrace samples and processes electrical signatures (voltage, current, power factor, and harmonic distortion) entirely on-device. The system provides real-time load characterization, early fault prediction, anomaly detection, and autonomous hardware protection without requiring continuous cloud connectivity.

---

## ✨ Key Features
* **Edge Physical AI Inference:** Real-time on-device classification and anomaly detection using TinyML / TensorFlow Lite Micro.
* **Autonomous Circuit Protection:** Sub-cycle fault detection and automatic relay cut-off for over-current, arc signatures, and voltage surges.
* **Zero-Latency & High Privacy:** Deterministic edge processing ensures electrical data is processed locally without external dependency.
* **Rich Telemetry & Reporting:** Standardized reporting via serial/MQTT for remote diagnostics and dashboard integration.

---

## 🏗️ Repository Architecture

```text
├── docs/                 # Documentation, schematic diagrams, and project report PDF
├── hardware/             # Circuit schematics, PCB layout files, and BOM
├── models/               # Quantized TinyML models (.tflite, .h header files)
├── src/                  # Firmware source code, DSP routines, and inference engine
├── .gitignore            # Git exclusion rules
├── CHANGELOG.md          # Version tracking and development history
├── CONTRIBUTING.md       # Contribution guidelines and coding standards
├── LICENSE               # Project license
├── README.md             # Main repository documentation
└── requirements.txt      # Python dependencies for model training and analysis
