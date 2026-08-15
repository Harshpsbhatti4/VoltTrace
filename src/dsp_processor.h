#pragma once
#include <Arduino.h>
#include <math.h>

struct ElectricalFeatures {
  float v_rms;
  float i_rms;
  float real_power;
  float apparent_power;
  float power_factor;
  float crest_factor;
  float form_factor;
  float peak_current;
};

class DSPProcessor {
public:
  static const int SAMPLES_PER_CYCLE = 64;
  static const int TOTAL_CYCLES = 3; 
  static const int TOTAL_SAMPLES = SAMPLES_PER_CYCLE * TOTAL_CYCLES;

  DSPProcessor(uint8_t v_pin, uint8_t i_pin, float v_calib = 220.0f, float i_calib = 30.0f)
    : voltage_pin(v_pin), current_pin(i_pin), v_calibration(v_calib), i_calibration(i_calib) {}

  ElectricalFeatures extractFeatures() {
    ElectricalFeatures feat;
    float sum_v_sq = 0.0f;
    float sum_i_sq = 0.0f;
    float sum_p = 0.0f;
    float sum_v_abs = 0.0f;
    float max_i = 0.0f;

    // Collect Synchronized Waveform Samples
    for (int k = 0; k < TOTAL_SAMPLES; k++) {
      // 10-bit or 12-bit ADC centered at VCC/2 (midpoint ~512 on 10-bit)
      float v_raw = ((float)analogRead(voltage_pin) - 512.0f) * (v_calibration / 512.0f);
      float i_raw = ((float)analogRead(current_pin) - 512.0f) * (i_calibration / 512.0f);

      sum_v_sq += v_raw * v_raw;
      sum_i_sq += i_raw * i_raw;
      sum_p += v_raw * i_raw;
      sum_v_abs += fabs(v_raw);

      if (fabs(i_raw) > max_i) {
        max_i = fabs(i_raw);
      }

      // Sampling timing adjustment for 50Hz grid
      delayMicroseconds(312); 
    }

    feat.v_rms = sqrt(sum_v_sq / TOTAL_SAMPLES);
    feat.i_rms = sqrt(sum_i_sq / TOTAL_SAMPLES);
    feat.real_power = fabs(sum_p / TOTAL_SAMPLES);
    feat.apparent_power = feat.v_rms * feat.i_rms;
    feat.peak_current = max_i;

    // Boundary-safe Power Factor calculation
    if (feat.apparent_power > 0.05f) {
      float raw_pf = feat.real_power / feat.apparent_power;
      feat.power_factor = constrain(raw_pf, 0.0f, 1.0f);
    } else {
      feat.power_factor = 1.0f;
    }

    // Crest Factor: Peak Current / RMS Current
    feat.crest_factor = (feat.i_rms > 0.05f) ? (feat.peak_current / feat.i_rms) : 1.414f;

    // Form Factor: RMS Voltage / Mean Absolute Voltage
    float v_mean_abs = sum_v_abs / TOTAL_SAMPLES;
    feat.form_factor = (v_mean_abs > 0.05f) ? (feat.v_rms / v_mean_abs) : 1.11f;

    return feat;
  }

private:
  uint8_t voltage_pin;
  uint8_t current_pin;
  float v_calibration;
  float i_calibration;
};
