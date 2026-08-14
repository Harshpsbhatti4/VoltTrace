# VoltTrace Hardware Design & Pinout

This directory contains the schematic designs, hardware Bill of Materials (BOM), and circuit interconnect specifications for the **VoltTrace** smart plug platform.

---

## Pin Mapping & Interfacing

| Subsystem | Sensor / Module | Arduino Pin / Interface | Signal Type |
| :--- | :--- | :--- | :--- |
| **Voltage Sensing** | ZMPT101B Module | `A0` | Analog (AC Sinusoid 0-5V biased) |
| **Current Sensing** | SCT-013-000 (with Burden) | `A1` | Analog (AC Sinusoid 0-5V biased) |
| **Actuator Control** | Fast-Switching Relay / SSR | `D7` | Digital Output (Active HIGH) |
| **Status Indicator** | Normal Operation (Green LED) | `D8` | Digital Output |
| **Status Indicator** | Fault / Cut-Off (Red LED) | `D9` | Digital Output |
| **Serial Telemetry** | Edge Logging / Debug | `TX / RX (UART)` | 115200 Baud |

---

## Electrical Safety & Isolation
* **Galvanic Isolation:** Voltage and current sensing channels are galvanically isolated via on-board transformers (ZMPT101B and Current Transformer) to protect low-voltage processing circuitry.
* **Control Isolation:** Relay triggers are optically coupled via optocouplers to prevent back-EMF and high-voltage transients from reaching the Arduino core.
* **Enclosure:** All high-voltage AC mains lines (220V–240V) must be housed inside an insulated, flame-retardant enclosure.
