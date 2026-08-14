#include "dsp_processor.h"

// Pin Definitions
#define PIN_VOLTAGE_ADC A0
#define PIN_CURRENT_ADC A1
#define PIN_RELAY       7
#define PIN_LED_OK      8
#define PIN_LED_FAULT   9

// Safety Limits
#define MAX_I_RMS_THRESHOLD    16.0f // 16 Amperes Max
#define VOLTAGE_SURGE_LIMIT    265.0f // 265V RMS
#define VOLTAGE_SAG_LIMIT      170.0f // 170V RMS

DSPProcessor dsp(PIN_VOLTAGE_ADC, PIN_CURRENT_ADC);

void setup() {
    Serial.begin(115200);

    pinMode(PIN_RELAY, OUTPUT);
    pinMode(PIN_LED_OK, OUTPUT);
    pinMode(PIN_LED_FAULT, OUTPUT);

    // Initial state: Relay energized (closed circuit), OK LED ON
    digitalWrite(PIN_RELAY, HIGH);
    digitalWrite(PIN_LED_OK, HIGH);
    digitalWrite(PIN_LED_FAULT, LOW);

    Serial.println(F("[VoltTrace] System Initialized. Running Edge Physical AI..."));
}

void triggerEmergencyCutoff(const char* reason) {
    digitalWrite(PIN_RELAY, LOW);     // Open circuit immediately
    digitalWrite(PIN_LED_OK, LOW);
    digitalWrite(PIN_LED_FAULT, HIGH); // Fault LED on

    Serial.print(F("[CRITICAL ALERT] Autonomous Cut-Off Triggered: "));
    Serial.println(reason);
}

bool runPhysicalAIInference(const ElectricalFeatures& feat) {
    // Edge TinyML model evaluation placeholder
    // Flag anomalous signatures (e.g. erratic Crest Factor + high Current)
    if (feat.crest_factor > 3.5f && feat.i_rms > 2.0f) {
        return false; // Anomaly detected
    }
    return true; // Normal operational baseline
}

void loop() {
    // 1. Digital Signal Processing & Feature Extraction
    ElectricalFeatures features = dsp.extractFeatures();

    // 2. Hardware Threshold Validation
    if (features.i_rms > MAX_I_RMS_THRESHOLD) {
        triggerEmergencyCutoff("Over-Current Detected");
        while (1) { delay(100); }
    }

    if (features.v_rms > VOLTAGE_SURGE_LIMIT || features.v_rms < VOLTAGE_SAG_LIMIT) {
        triggerEmergencyCutoff("Voltage Deviation Outside Safe Range");
        while (1) { delay(100); }
    }

    // 3. Physical AI Model Evaluation
    bool isNormal = runPhysicalAIInference(features);
    if (!isNormal) {
        triggerEmergencyCutoff("AI Anomaly Detected (Electrical Arc / Waveform Distortion)");
        while (1) { delay(100); }
    }

    // 4. Telemetry Output (Serial / Non-blocking)
    Serial.print(F("Vrms: ")); Serial.print(features.v_rms, 1);
    Serial.print(F("V | Irms: ")); Serial.print(features.i_rms, 2);
    Serial.print(F("A | P: ")); Serial.print(features.real_power, 1);
    Serial.print(F("W | PF: ")); Serial.print(features.power_factor, 2);
    Serial.print(F(" | CF: ")); Serial.println(features.crest_factor, 2);

    delay(200);
}
