# VoltTrace ⚡
> **Edge-Powered Smart Plug Platform with Embedded Physical AI**  
> *Developed for the Arduino Physical AI Challenge India 2026*

---

## 📌 Abstract
**VoltTrace** is an intelligent, edge-controlled smart energy monitor and safety plug. By integrating physical AI directly onto the microcontroller, VoltTrace analyzes electrical signatures (voltage, current, power factor, and harmonics) in real time. It detects anomalous loads, predicts device degradation, prevents electrical hazards, and performs localized inference without relying on persistent cloud connectivity.

---

## ✨ Key Features
* **Real-Time Edge Inference:** Local processing of electrical parameters for anomaly detection and load classification.
* **Autonomous Safety Protection:** Instant cut-off during over-current, voltage spikes, or abnormal waveform signatures.
* **Low Latency & High Privacy:** Critical inference runs locally on the hardware, keeping telemetry private and deterministic.
* **Lightweight Telemetry:** Selective reporting of insights and metrics via MQTT/serial to cloud dashboards or gateways.

---

## 🏗️ Repository Architecture

```text
├── docs/                 # Documentation, schematic diagrams, and project report PDF
├── hardware/             # Circuit schematics, PCB layouts, and Bill of Materials (BOM)
├── models/               # Pre-trained TinyML / Physical AI models (.tflite, .h)
├── src/                  # Source code (firmware, DSP, inference pipelines)
├── .gitignore            # Git ignore file
├── CHANGELOG.md          # Version history and milestone tracking
├── CONTRIBUTING.md       # Contribution guidelines
├── LICENSE               # Project license (e.g., MIT, Apache-2.0)
├── README.md             # Main project documentation
└── requirements.txt      # Python/toolchain dependencies for training & testing

```

---

## 🛠️ Hardware Stack & Components

* **Core Controller:** Arduino UNO Q / Compatible Edge Processing Board
* **Sensing Unit:** Non-invasive Current Sensor (CT / Rogowski coil), AC Voltage Sensing Transformer/ZMPT101B
* **Actuation:** High-current Relay / Solid State Switch
* **Power Management:** Isolated AC-DC Step-down module

---

## 🚀 Getting Started

### 1. Prerequisites

* **Arduino IDE 2.x** or **PlatformIO** installed.
* **Python 3.10+** (if training or quantizing custom edge models).

### 2. Installation & Setup

1. Clone the repository:
```bash
git clone [https://github.com/](https://github.com/)<your-username>/VoltTrace.git
cd VoltTrace

```


2. Install host Python dependencies (for model export / data logging):
```bash
pip install -r requirements.txt

```


3. Open `src/` in the Arduino IDE or PlatformIO, select your board target, and upload the firmware.

---

## 📊 Physical AI Pipeline

1. **Signal Acquisition:** High-rate sampling of AC voltage and current waveforms.
2. **Feature Extraction:** On-device computation of RMS values, active/reactive power, Crest Factor, and FFT harmonics.
3. **Model Inference:** Embedded TensorFlow Lite Micro / TinyML model evaluates feature vectors to classify connected loads and flag abnormal behaviors.
4. **Action Trigger:** Immediate autonomous relay cut-off if safety thresholds or anomaly confidence limits are exceeded.

---

## 📄 Documentation & Submissions

* Detailed project report: Located under [`docs/`](https://www.google.com/search?q=docs/)
* Milestone progress: Documented in [`CHANGELOG.md`](CHANGELOG.md)

---

## 📜 License

This project is licensed under the terms of the [MIT License](https://www.google.com/search?q=LICENSE).

```

```
