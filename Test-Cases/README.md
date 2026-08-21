# VoltTrace Test Cases & Diagnostic Validation

This directory contains the experimental test logs, video recordings, and diagnostic telemetry captures collected during the validation of the **VoltTrace Edge-AI Smart Plug Platform**. 

The test suite evaluates the dual-core pipeline—from raw MCU analog signal acquisition and noise-clamping to the MPU Random Forest NILM classifier, Autoencoder anomaly scoring, and autonomous hardware relay protection.

---

## Test Suite Overview Matrix

| Test Case | Scenario | Load Category | Desirable Outcome | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | **Mains OFF / No AC** | Open Circuit | Zeroed telemetry ($V=0\text{V}, I=0\text{A}$) & $100\%$ Health | $V=0\text{V}, I=0\text{A}$, Standby State | **PASS** |
| **TC-02** | **Mains ON / No Load** | Idle Socket | Baseline noise clamped to $0.000\text{A}$; $100\%$ Health | $I_{RMS}=0.000\text{A}$, `NO LOAD DETECTED` | **PASS** |
| **TC-03** | **Incandescent Bulb** | Resistive (Thermal) | Pure resistive classification ($PF \approx 0.99, CF \approx 1.41$) | $100\%$ Health, `Resistive Load` | **PASS** |
| **TC-04** | **Fused Incandescent** | Broken Filament Fault | $0\text{A}$ current draw under active voltage; $0\%$ Health | $0\%$ Health, `NO LOAD DETECTED` | **PASS** |
| **TC-05** | **Mobile Phone Charger** | Non-Linear SMPS | Identify non-linear pulse ($CF > 3.0$); $100\%$ Health | `Capacitive / Non-Linear` identified | **PASS** |
| **TC-06** | **LED Lighting** | Pulsed Harmonic | Classify non-linear load; lock fingerprint state | `LED Lighting / SMPS` locked steady | **PASS** |
| **TC-07** | **Landline Adapter** | Ultra-Low Power SMPS | Maintain state despite grid fluctuations | State held; brownout warning logged | **PASS** |

---

## Detailed Test Case Breakdowns

### Test Case 01: Mains OFF / No AC
* **Setup**: Circuit powered down; no load connected; mains supply turned off.
* **Desirable Outcome**: Both voltage and current read strictly $0$, placing the system in an optimal standby state with a $100\%$ Universal Health Score.
* **Actual Output**:
  * **$V_{RMS}$**: $0.0\text{ V}$ ($0.00\text{ p.u.}$)
  * **$I_{RMS}$**: $0.000\text{ A}$ ($0.00\text{ p.u.}$)
  * **Health Score**: $100\%$
  * **UI Classification**: `NO LOAD DETECTED`
* **Technical Reasoning**: Low-voltage threshold rules in `sketch.ino` ($V_{RMS} < 140\text{V}$) zeroed all power calculations, preventing floating ADC values from generating false telemetry.

---

### Test Case 02: Mains ON / No Load (Idle Socket)
* **Setup**: Mains voltage active ($\sim 230\text{V}$); open socket with no physical appliance plugged in.
* **Desirable Outcome**: Detect live line voltage while completely clamping ambient CT sensor noise to report $0.000\text{A}$ current and $100\%$ health.
* **Actual Output**:
  * **$V_{RMS}$**: $211.5\text{ V} - 230.0\text{ V}$
  * **$I_{RMS}$**: $0.000\text{ A}$
  * **Health Score**: $100\%$
  * **UI Classification**: `NO LOAD DETECTED`
* **Technical Reasoning**: Standard current transformers (CTs) produce floating DC offset noise ($\sim 0.19\text{A}$) at zero current. Raising the software noise gate threshold to $0.22\text{A}$ in `sketch.ino` cleanly clamped ambient noise to zero, bypassing false ML diagnostic triggers.

---

### Test Case 03: Incandescent Bulb (Working Filament)
* **Setup**: $100\text{W}$ incandescent light bulb connected to the active smart plug socket.
* **Desirable Outcome**: Correctly classify the load as a pure resistive element with high power factor ($\approx 1.0$) and pure sinusoidal crest factor ($\approx 1.414$).
* **Actual Output**:
  * **$V_{RMS}$**: $228.4\text{ V}$
  * **$I_{RMS}$**: $0.412\text{ A}$
  * **Power Factor ($PF$)**: $0.99$
  * **Crest Factor ($CF$)**: $1.41$
  * **Health Score**: $100\%$ (`OPTIMAL HEALTH`)
  * **Identified Load**: `Incandescent Bulb (100W/200W)` / `Resistive (Thermal)`
* **Technical Reasoning**: The linear current waveform resulted in near-unity power factor and ideal crest factor, matching the baseline Autoencoder profile and generating a near-zero anomaly score.

---

### Test Case 04: Fused / Broken Incandescent Bulb
* **Setup**: Incandescent bulb with a physically broken (fused) filament plugged into the socket under active mains voltage.
* **Desirable Outcome**: System detects line voltage presence alongside total absence of current flow, immediately marking the state as an open circuit fault ($0\%$ health).
* **Actual Output**:
  * **$V_{RMS}$**: $270.2\text{ V}$
  * **$I_{RMS}$**: $0.000\text{ A}$
  * **Health Score**: $0\%$ (`NO LOAD DETECTED`)
  * **AI Status Message**: `Open Circuit / Idle Socket: No active current draw detected.`
* **Technical Reasoning**: The broken filament interrupted the current path. Although voltage was sensed at the terminals, the lack of current triggered the open-circuit logic in `run_ml_diagnostics()`, confirming an inoperative load.

---

### Test Case 05: Mobile Phone Charger
* **Setup**: Switched-mode power supply (SMPS) mobile fast charger plugged into the socket.
* **Desirable Outcome**: Recognize low-power, high-frequency harmonic switching characteristics without raising false overcurrent or power factor alarms.
* **Actual Output**:
  * **$I_{RMS}$**: $0.120\text{ A} - 0.180\text{ A}$
  * **Crest Factor ($CF$)**: $3.45$
  * **Health Score**: $100\%$ (`OPTIMAL HEALTH`)
  * **Identified Load**: `LED Lighting / SMPS` / `Capacitive / Non-Linear`
* **Technical Reasoning**: Non-linear SMPS rectification draws current in sharp, narrow pulses. The higher crest factor ($>3.0$) matched the trained Random Forest non-linear decision boundary. Reference power scaling ($P_{ref} = 50\text{W}$) prevented false degradation penalties.

---

### Test Case 06: LED Lighting Bulb
* **Setup**: $9\text{W} - 12\text{W}$ commercial LED light bulb plugged into the socket.
* **Desirable Outcome**: Classify non-linear load profile and lock fingerprint state across fluctuating current readings without dropping back to "Standby."
* **Actual Output**:
  * **$I_{RMS}$**: $0.080\text{ A} - 0.223\text{ A}$
  * **Crest Factor ($CF$)**: $4.48$
  * **Health Score**: $100\%$ (`OPTIMAL HEALTH`)
  * **Identified Load**: `LED Lighting / SMPS`
* **Technical Reasoning**: High peak-to-RMS ratio confirmed the presence of harmonic diode bridge charging pulses. The integration of Exponential Moving Average (EMA) current hysteresis in `main.py` prevented single-cycle sensor micro-drops from resetting the active diagnostic session.

---

### Test Case 07: Landline Power Adapter
* **Setup**: Ultra-low-power ($<5\text{W}$) landline phone transformer/adapter plugged into the socket during local mains grid brownout conditions ($\sim 188\text{V}$).
* **Desirable Outcome**: Maintain load classification while accurately identifying grid voltage deviation (`MAINS_VOLTAGE_OUT_OF_BAND`).
* **Actual Output**:
  * **$V_{RMS}$**: $188.7\text{ V}$ ($0.82\text{ p.u.}$)
  * **$I_{RMS}$**: $0.223\text{ A}$
  * **Power Factor ($PF$)**: $0.10$
  * **Health Score**: $64\%$ (`DEGRADED STATE`)
  * **AI Status Message**: `WARNING: Telemetry deviating from operational baseline (0.820 p.u. V).`
* **Technical Reasoning**: The load fingerprint lock successfully held the `LED Lighting / SMPS` classification. The MPU rule engine detected $V_{norm} < 0.85\text{ p.u.}$ and lowered the health score to $64\%$, demonstrating real-time grid fault monitoring.
