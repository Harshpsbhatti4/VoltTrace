#include "dsp_processor.h"

// Pin Definitions
#define PIN_VOLTAGE_ADC A0
#define PIN_CURRENT_ADC A1
#define PIN_RELAY       7
#define PIN_LED_NORMAL  8
#define PIN_LED_FAULT   9

// Critical Hardware Safety Thresholds
#define MAX_I_RMS_LIMIT       16.0f   // 16 Amperes continuous
#define VOLTAGE_SURGE_LIMIT   265.0f  // Over-voltage threshold
#define VOLTAGE_SAG_LIMIT     165.0f  // Under-voltage threshold

DSPProcessor dsp(PIN_VOLTAGE_ADC, PIN_CURRENT_ADC, 230.0f, 30.0f);

void triggerEmergencyCutoff(const char* reason) {
  digitalWrite(PIN_RELAY, LOW);       // Isolate load immediately
  digitalWrite(PIN_LED_NORMAL, LOW);
  digitalWrite(PIN_LED_FAULT, HIGH);  // Red Alert indicator

  Serial.print(F("[CRITICAL FAULT] Autonomous Cut-off: "));
  Serial.println(reason);
}

// Physical-AI Inference Evaluator (Feature Space Vector Verification)
bool runPhysicalAIInference(const ElectricalFeatures& feat) {
  // Anomaly Vector Check 1: Severe Waveform Distortion (Arcing / Tripping)
  if (feat.crest_factor > 3.2f && feat.i_rms > 1.0f) {
    return false; // Fault detected
  }

  // Anomaly Vector Check 2: Reactive Degradation & Poor Power Factor
  if (feat.power_factor < 0.40f && feat.i_rms > 3.0f) {
    return false; // Severe reactive fault / motor stalling
  }

  // Anomaly Vector Check 3: Voltage Form Factor Deviation
  if (feat.form_factor > 1.45f || feat.form_factor < 0.95f) {
    return false; // Grid harmonic distortion / clipping
  }

  return true; // Healthy baseline
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_LED_NORMAL, OUTPUT);
  pinMode(PIN_LED_FAULT, OUTPUT);

  // Initial State: Energized (Normal Operation)
  digitalWrite(PIN_RELAY, HIGH);
  digitalWrite(PIN_LED_NORMAL, HIGH);
  digitalWrite(PIN_LED_FAULT, LOW);

  Serial.println(F("[VoltTrace System Initialized]"));
  Serial.println(F("V_RMS,I_RMS,P_ACT,PF,CREST_FACTOR,FORM_FACTOR,STATUS"));
}

void loop() {
  // 1. Digital Signal Processing Feature Extraction
  ElectricalFeatures feat = dsp.extractFeatures();

  // 2. Hardware Threshold Protection (Sub-cycle response)
  if (feat.i_rms > MAX_I_RMS_LIMIT) {
    triggerEmergencyCutoff("Over-Current Detected (>16A)");
    while (1) delay(100);
  }

  if (feat.v_rms > VOLTAGE_SURGE_LIMIT || feat.v_rms < VOLTAGE_SAG_LIMIT) {
    triggerEmergencyCutoff("Voltage Threshold Breach");
    while (1) delay(100);
  }

  // 3. Physical AI Micro-Inference
  bool isHealthy = runPhysicalAIInference(feat);
  if (!isHealthy) {
    triggerEmergencyCutoff("Physical-AI Anomaly Vector Detected (Arcing/Degradation)");
    while (1) delay(100);
  }

  // 4. Real-time Telemetry Stream (CSV Format over Serial)
  Serial.print(feat.v_rms, 1);
  Serial.print(F(","));
  Serial.print(feat.i_rms, 2);
  Serial.print(F(","));
  Serial.print(feat.real_power, 1);
  Serial.print(F(","));
  Serial.print(feat.power_factor, 2);
  Serial.print(F(","));
  Serial.print(feat.crest_factor, 2);
  Serial.print(F(","));
  Serial.print(feat.form_factor, 2);
  Serial.print(F(","));
  Serial.println(isHealthy ? F("NORMAL") : F("FAULT"));

  delay(200);
}
