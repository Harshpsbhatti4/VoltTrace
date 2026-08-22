# VoltTrace: Hardware Demo Recordings & Test Case Validation

**Project Title:** VoltTrace - Edge-Powered Physical AI Smart Plug  
**Hardware Platform:** Dual-Core Arduino UNO Q (Microcontroller Unit + Linux Microprocessor Unit)  
**Public Google Drive Demo Folder:** [https://drive.google.com/drive/folders/1mKykndEL4rWojgVOP0nfab-3UPmW3atM?usp=sharing]

---

## Overview

This repository contains the official hardware test recordings for **VoltTrace**, captured directly from the on-device web dashboard served on port `7000`. The system uses Non-Intrusive Load Monitoring (NILM) powered by Random Forest classification and Autoencoder reconstruction neural networks to evaluate household appliance health and execute sub-cycle circuit safety completely offline.

---

## Test Cases, Inputs, and Verified Outputs

| Test Case Video File | Hardware Test Input Condition | Expected System Behavior | Actual Observed Output & Results | System Status |
| :--- | :--- | :--- | :--- | :--- |
| **`1.Mains_OFF_Load_OFF.mp4`** | $0\text{V}$ AC Mains input, $0\text{A}$ Load Current (Unpowered state) | Suppress ML inference; enforce hard circuit gate to prevent false fault triggers. | **RMS Voltage:** $0.0\text{V}$ <br> **RMS Current:** $0.000\text{A}$ <br> **Health Score:** `NO LOAD DETECTED` <br> **Classification:** `NO LOAD DETECTED` | **PASS** |
| **`2.Mains_ON_Load_OFF.mp4`** | $230\text{V}$ AC Mains powered, Open output socket ($0\text{A}$ Load Current) | Continuous AC voltage stream monitoring; standby state locked until test initialized. | **RMS Voltage:** $\sim 230.0\text{V}$ ($1.0\text{ p.u.}$) <br> **RMS Current:** $0.000\text{A}$ <br> **Health Score:** `NO LOAD DETECTED` <br> **Appliance:** `No Load Detected` | **PASS** |
| **`4.Load_Sample_02-Fused_Incandescent_Bulb.mp4`** | Blown/Fused $100\text{W}$ Incandescent Bulb inserted into socket | Open circuit detection despite resistive thermal load profile expectation. | **RMS Current:** $0.000\text{A}$ <br> **Power:** $0.0\text{W}$ <br> **Health Score:** `NO LOAD DETECTED` <br> **Diagnostics:** Open element flagged without throwing false overcurrent trip. | **PASS** |
| **`5.Load_Sample_03-Phone_Charger.mp4`** | Low-power Switched-Mode Power Supply (SMPS) load | Extract non-linear harmonic profile, high Crest Factor, and low Power Factor. | **Power:** $\sim 5\text{--}15\text{W}$ <br> **Crest Factor:** $> 2.50$ <br> **Appliance:** `LED Lighting / SMPS` <br> **Category:** `Capacitive / Non-Linear` <br> **Health Score:** $95.0\text{--}98.0\%$ (`OPTIMAL HEALTH`) | **PASS** |
| **`6.Load_Sample_04-LED_Bulb.mp4`** | $9\text{W--12W}$ Commercial LED Bulb connected | Non-linear load profiling with capacitive displacement. | **RMS Current:** $\sim 0.050\text{--}0.090\text{A}$ <br> **Power Factor:** $0.50\text{--}0.68$ <br> **Appliance:** `LED Lighting / SMPS` <br> **Health Score:** $96.0\%$ (`OPTIMAL HEALTH`) | **PASS** |
| **`7.Load_Sample_05-Cordless_Landline.mp4`** | Constant low-power base station AC adapter | Detect low-power continuous linear/capacitive footprint. | **RMS Current:** Low steady-state draw <br> **Appliance:** Identified under capacitive/SMPS profile family <br> **Health Score:** $96.0\%$ (`OPTIMAL HEALTH`) | **PASS** |

---

## Technical Features Demonstrated

1. **Hard No-Load Circuit Gate:** Prevents false positive autoencoder flags ($10\%$ health drops) when appliances are unplugged or idle by isolating $I < 0.05\text{A}$ states.
2. **Autonomous NILM Classification:** Accurately distinguishes non-linear capacitive loads (chargers, LEDs) from resistive heating/lighting elements based on $V_{RMS}$, $I_{RMS}$, Active Power, Power Factor, and Crest Factor.
3. **On-Device Diagnostics:** Runs Scikit-Learn models and FastAPI directly on the dual-core Arduino UNO Q's Linux environment with zero cloud connectivity required.
