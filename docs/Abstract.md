# VoltTrace: Edge-Powered Physical AI Smart Energy & Safety Plug
**Challenge:** Arduino Physical AI Challenge India 2026  
**Target Hardware:** Arduino UNO Q / Edge Microcontroller  
**Document Version:** 1.0.0  

---

## 1. Executive Summary
**VoltTrace** is an intelligent, edge-native smart plug and electrical safety platform designed to bring autonomous Physical AI to modern power systems. Traditional smart plugs merely measure static power metrics and offload telemetry to cloud servers for processing, introducing network latency, privacy vulnerabilities, and cloud dependency. VoltTrace solves this by executing real-time digital signal processing (DSP) and quantized machine learning directly on the embedded microcontroller. By analyzing high-frequency AC electrical signatures (voltage, current, crest factor, and harmonic distortions), VoltTrace classifies operational loads, identifies electrical anomalies, and initiates sub-cycle hardware protection locally.

---

## 2. Problem Statement
* **Safety Latency:** Critical electrical faults (e.g., arc faults, abnormal surges, overheating degradation) require sub-second intervention. Cloud-reliant processing introduces network latency that fails to prevent hardware damage or fire hazards.
* **Lack of Granular Load Insight:** Standard energy meters report aggregate consumption without understanding the health or identity of the attached appliance.
* **Privacy & Network Overhead:** Continuously streaming raw high-rate electrical waveform data to the cloud consumes significant bandwidth and exposes private household/industrial behavior.

---

## 3. The Physical AI Solution
VoltTrace implements an end-to-end TinyML pipeline directly on the edge hardware:

1. **Synchronous Signal Acquisition:** Continuous, phase-aligned sampling of AC voltage and load current waveforms.
2. **On-Device Feature Engineering:** Real-time extraction of key electrical metrics including RMS Voltage/Current, Active/Reactive Power, Crest Factor, Form Factor, and spectral characteristics.
3. **Embedded TinyML Inference:** A quantized TensorFlow Lite Micro neural network evaluates the extracted feature vectors to classify appliance types and detect anomalous operating states.
4. **Autonomous Edge Actuation:** A hardware interrupt-driven protection loop triggers an on-board relay/SSR immediately upon detecting dangerous fault signatures, operating independently of network connectivity.

---

## 4. Key Technical Specifications
| Parameter | Specification |
| :--- | :--- |
| **Operating Voltage** | 220V - 240V AC, 50 Hz |
| **Current Rating** | Up to 16A Continuous |
| **Processing Core** | Arduino UNO Q (Physical AI / Edge ML Capable) |
| **Inference Engine** | TensorFlow Lite Micro / C++ Edge Model |
| **Sampling & DSP** | High-frequency AC channel sampling, RMS & harmonic extraction |
| **Actuation Time** | Sub-cycle autonomous cut-off (< 20 ms) |
| **Connectivity** | Local Serial Telemetry / MQTT Gateway (Non-blocking) |

---

## 5. Impact & Application
* **Smart Home & Consumer Safety:** Prevents appliance damage and household electrical fires via immediate anomaly cut-off.
* **Industrial Preventive Maintenance:** Detects motor degradation, pump cavitation, or abnormal transformer loads before catastrophic failure.
* **Autonomous Reliability:** Fully operational in offline environments without external internet connectivity.
