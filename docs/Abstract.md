# VoltTrace | Project Abstract

> **Project Title**: VoltTrace: Edge-Powered Smart Plug Platform with Embedded Physical AI  
> **Target Event**: Arduino Physical AI Challenge India 2026  
> **Hardware Platform**: Arduino UNO Q (Dual-Core MCU + MPU)  

---

## Executive Summary

**VoltTrace** is an edge-controlled smart energy monitoring and safety plug platform designed to deliver real-time electrical safety diagnostics and Non-Intrusive Load Monitoring (NILM) entirely on-device. Developed to address the limitations of cloud-dependent smart plugs—such as latency, privacy vulnerabilities, and loss of safety cut-off capabilities during internet outages—VoltTrace deploys Physical AI directly onto embedded hardware.

By harnessing the dual-core architecture of the **Arduino UNO Q**, raw 10-bit analog voltage and current waveforms sampled at high frequency on the microcontroller (MCU) core stream via Inter-Process Communication (IPC) over RouterBridge to a Linux microprocessor (MPU) core. The MPU executes a dual-stage machine learning engine consisting of a Random Forest NILM Classifier for load fingerprinting and load-specific Autoencoders for anomaly detection.

The platform continuously evaluates electrical parameters—including RMS voltage, RMS current, active power, power factor, and crest factor—to generate a real-time **Universal Health Score ($0\% - 100\%$)**. In the event of critical anomalies such as overcurrent, thermal runaway, or severe line voltage degradation, VoltTrace executes sub-cycle hardware protection by actuating an on-board safety relay, isolating the connected load without requiring cloud connectivity.

---

## Key Technical Objectives & Innovation

* **Zero-Cloud Physical AI**: Complete local inference ensures zero latency for emergency trips, $100\%$ operational uptime during network failures, and absolute data privacy.
* **Heterogeneous Dual-Core Pipeline**: Microsecond-level analog signal acquisition and signal conditioning handled by C++/Zephyr on the MCU core, offloading heavy ML inference and Web UI hosting to Python/FastAPI on the MPU core.
* **Autonomous Load Fingerprinting**: Automated identification of resistive, inductive, and non-linear switched-mode power supply (SMPS) appliances using time-domain harmonic signatures and crest factors.
* **Universal Health & Anomaly Scoring**: Autoencoder reconstruction loss mapping that quantifies appliance health degradation and identifies early equipment failures before catastrophic breakdown occurs.

---

## Target Applications

1. **Industrial Equipment Diagnostics**: Early fault detection for motor drives, pumps, and heating elements.
2. **Smart Home Safety**: Real-time arc signature, overvoltage, and thermal runaway prevention for consumer electronics.
3. **Energy Management Systems**: Autonomous load profiling and granular power consumption tracking at the socket level.
