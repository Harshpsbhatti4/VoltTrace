# VoltTrace | Hardware & Circuit Schematic Documentation

This document outlines the circuit layout, sensor signal conditioning, and pin interfaces for the **VoltTrace Edge-AI Smart Plug Platform**.

---

## 1. Complete System Pinout Matrix

| Module / Component | Module Pin | Arduino UNO Q Pin | Signal Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| **ZMPT101B Voltage Module** | `OUT` | `A2` | Analog Input | Scaled AC Voltage Waveform |
| **ACS712 Current Sensor** | `OUT` | `A1` | Analog Input | Biased AC Current Waveform |
| **5V Single-Channel Relay** | `IN` | `D7` | Digital Output | Active HIGH Relay Trigger (`HIGH` = Closed, `LOW` = Trip) |
| **Sensor VCC Lines** | `VCC` | `5V` | DC Power Output | $+5\text{V}$ Logic Power Supply |
| **Sensor GND Lines** | `GND` | `GND` | Ground | Common System Ground Reference |

---

## 2. Signal Conditioning & Analog Front End (AFE)

### Voltage Sensing (ZMPT101B)
* **Galvanic Isolation**: Integrated voltage transformer provides $2\text{kV}$ physical isolation between mains AC ($230\text{V RMS}$) and low-voltage logic.
* **Calibration**: Trimpot tuned so that nominal $230\text{V RMS}$ produces a peak-to-peak AC swing centered around $+2.5\text{V DC}$ ($512$ ADC count).

### Current Sensing (ACS712 Hall-Effect Module)
* **Inline Sensing**: ACS712 Hall-effect sensor measures AC line current directly through low-resistance copper conductors.
* **DC Offset**: Output outputs a static zero-current voltage bias of $V_{CC} / 2 = 2.5\text{V DC}$. 
* **MCU Sampling**: The 10-bit ADC samples both positive and negative AC half-cycles without negative voltage clipping.

---

## 3. Hardware Fail-Safe Mechanism

* **Active Relay Line**: Digital Pin `D7` controls the main load relay.
* **Hardware Interlock**: Under overcurrent ($I > I_{limit}$), thermal runaway ($T > 85^\circ\text{C}$), or code crash conditions, Pin `D7` drops `LOW`, cutting power to the socket.
