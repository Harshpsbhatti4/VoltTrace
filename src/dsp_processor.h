#pragma once
#include <Arduino.h>

struct ElectricalFeatures {
    float v_rms;
    float i_rms;
    float real_power;
    float apparent_power;
    float power_factor;
    float crest_factor;
    float peak_current;
};

class DSPProcessor {
public:
    static const int SAMPLES_PER_CYCLE = 64;
    static const int TOTAL_SAMPLES = 128; // 2 complete 50Hz cycles

    DSPProcessor(uint8_t v_pin, uint8_t i_pin, float v_calib = 220.0f, float i_calib = 30.0f)
        : voltage_pin(v_pin), current_pin(i_pin), v_calibration(v_calib), i_calibration(i_calib) {}

    ElectricalFeatures extractFeatures() {
        ElectricalFeatures feat;
        float sum_v_sq = 0.0f;
        float sum_i_sq = 0.0f;
        float sum_p = 0.0f;
        float max_i = 0.0f;

        // Collect synchronized samples
        for (int k = 0; k < TOTAL_SAMPLES; k++) {
            // Read analog raw (assuming 10-bit / 12-bit ADC centered at VCC/2)
            float raw_v = (analogRead(voltage_pin) - 512.0f) * (v_calibration / 512.0f);
            float raw_i = (analogRead(current_pin) - 512.0f) * (i_calibration / 512.0f);

            sum_v_sq += raw_v * raw_v;
            sum_i_sq += raw_i * raw_i;
            sum_p += raw_v * raw_i;

            float abs_i = fabs(raw_i);
            if (abs_i > max_i) {
                max_i = abs_i;
            }

            delayMicroseconds(312); // Sample spacing for ~3.2kHz sampling
        }

        feat.v_rms = sqrt(sum_v_sq / TOTAL_SAMPLES);
        feat.i_rms = sqrt(sum_i_sq / TOTAL_SAMPLES);
        feat.real_power = sum_p / TOTAL_SAMPLES;
        feat.apparent_power = feat.v_rms * feat.i_rms;
        feat.power_factor = (feat.apparent_power > 0.01f) ? (feat.real_power / feat.apparent_power) : 1.0f;
        feat.peak_current = max_i;
        feat.crest_factor = (feat.i_rms > 0.01f) ? (max_i / feat.i_rms) : 1.0f;

        return feat;
    }

private:
    uint8_t voltage_pin;
    uint8_t current_pin;
    float v_calibration;
    float i_calibration;
};
