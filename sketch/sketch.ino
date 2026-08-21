#include <Arduino.h>
#include <Arduino_RouterBridge.h>

const uint8_t PIN_VOLTAGE = A2;  
const uint8_t PIN_CURRENT = A1;  
const uint8_t PIN_RELAY   = 7;   

float V_CALIBRATION = 122.60f; 
float I_CALIBRATION = 0.0488f;  

const int TOTAL_SAMPLES = 192;   
const unsigned long TELEMETRY_INTERVAL_MS = 250; 
unsigned long lastTelemetryTime = 0;

void setup() {
    Monitor.begin();
    Bridge.begin();

    #if defined(analogReadResolution)
        analogReadResolution(10); 
    #endif

    pinMode(PIN_RELAY, OUTPUT);
    digitalWrite(PIN_RELAY, HIGH); 

    Monitor.println("VoltTrace Engine Calibrated & Initialized...");
}

void loop() {
    unsigned long currentMillis = millis();

    if (currentMillis - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
        lastTelemetryTime = currentMillis;

        int min_v = 1023, max_v = 0;
        int min_i = 1023, max_i = 0;
        long sum_v_raw = 0;
        long sum_i_raw = 0;

        int v_samples[TOTAL_SAMPLES];
        int i_samples[TOTAL_SAMPLES];

        for (int k = 0; k < TOTAL_SAMPLES; k++) {
            analogRead(PIN_VOLTAGE);
            delayMicroseconds(15);
            int raw_v = analogRead(PIN_VOLTAGE);

            analogRead(PIN_CURRENT);
            delayMicroseconds(15);
            int raw_i = analogRead(PIN_CURRENT);

            v_samples[k] = raw_v;
            i_samples[k] = raw_i;

            sum_v_raw += raw_v;
            sum_i_raw += raw_i;

            if (raw_v < min_v) min_v = raw_v;
            if (raw_v > max_v) max_v = raw_v;
            if (raw_i < min_i) min_i = raw_i;
            if (raw_i > max_i) max_i = raw_i;

            delayMicroseconds(200);
        }

        float v_bias = (float)sum_v_raw / TOTAL_SAMPLES;
        float i_bias = (float)sum_i_raw / TOTAL_SAMPLES;

        int v_pp = max_v - min_v;
        int i_pp = max_i - min_i;

        float sum_v_sq = 0.0f;
        float sum_i_sq = 0.0f;
        float sum_p    = 0.0f;
        float max_abs_i = 0.0f;

        for (int k = 0; k < TOTAL_SAMPLES; k++) {
            float v_inst = (v_samples[k] - v_bias) * V_CALIBRATION;
            float i_inst = (i_samples[k] - i_bias) * I_CALIBRATION;

            sum_v_sq += v_inst * v_inst;
            sum_i_sq += i_inst * i_inst;
            sum_p    += v_inst * i_inst;

            if (fabsf(i_inst) > max_abs_i) {
                max_abs_i = fabsf(i_inst);
            }
        }

        float v_rms = sqrtf(sum_v_sq / TOTAL_SAMPLES);
        float i_rms = sqrtf(sum_i_sq / TOTAL_SAMPLES);
        float p_act = fabsf(sum_p / TOTAL_SAMPLES);

        if (v_rms < 140.0f || v_pp < 5) {
            v_rms = 0.0f;
            p_act = 0.0f;
        }

        if (i_rms < 0.22f || i_pp < 4 || v_rms == 0.0f) {
            i_rms = 0.0f;
            p_act = 0.0f;
            max_abs_i = 0.0f;
        }

        float s_app = v_rms * i_rms;
        float pf = (s_app > 0.5f) ? constrain(p_act / s_app, 0.0f, 1.0f) : 1.0f;
        float crest_factor = (i_rms > 0.05f) ? constrain(max_abs_i / i_rms, 1.0f, 4.5f) : 1.414f;
        float temperature = 28.5f + (i_rms * 1.5f);

        Monitor.print("V_RMS: ");
        Monitor.print(v_rms, 1);
        Monitor.print(" V | I_RMS: ");
        Monitor.print(i_rms, 3);
        Monitor.print(" A | Power: ");
        Monitor.print(p_act, 1);
        Monitor.println(" W");

        Bridge.notify("record_telemetry", v_rms, i_rms, p_act, pf, crest_factor, temperature);
    }
}
