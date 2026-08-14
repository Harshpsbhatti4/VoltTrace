import numpy as np
import tensorflow as tf
from tensorflow import keras

# 1. Synthetic dataset generator for baseline electrical load features:
# [V_rms_norm, I_rms_norm, P_active_norm, PF, Crest_Factor, Form_Factor]
def generate_synthetic_data(samples=1000):
    X = []
    y = []
    for _ in range(samples):
        # Normal operational profiles (Label 0)
        if np.random.rand() > 0.3:
            v_rms = np.random.uniform(0.9, 1.05)
            i_rms = np.random.uniform(0.1, 0.8)
            pf = np.random.uniform(0.85, 0.99)
            p_act = v_rms * i_rms * pf
            cf = np.random.uniform(1.3, 1.6)
            ff = np.random.uniform(1.05, 1.15)
            label = 0
        # Anomaly profiles (Arcing / Degradation / Faults) (Label 1)
        else:
            v_rms = np.random.uniform(0.7, 1.15)
            i_rms = np.random.uniform(0.5, 1.5)
            pf = np.random.uniform(0.3, 0.75)
            p_act = v_rms * i_rms * pf
            cf = np.random.uniform(2.5, 4.5)  # High spikes/crest factor
            ff = np.random.uniform(1.3, 1.8)
            label = 1

        X.append([v_rms, i_rms, p_act, pf, cf, ff])
        y.append(label)

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)


X_train, y_train = generate_synthetic_data(2000)

# 2. Lightweight Edge Neural Network Architecture
model = keras.Sequential(
    [
        keras.layers.Input(shape=(6,)),
        keras.layers.Dense(12, activation="relu"),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(2, activation="softmax"),
    ]
)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.fit(X_train, y_train, epochs=25, batch_size=16, verbose=1)

# 3. Post-Training INT8 Quantization for Arduino Deployment
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]


def representative_data_gen():
    for i in range(100):
        yield [X_train[i : i + 1]]


converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_quant_model = converter.convert()

with open("models/model.tflite", "wb") as f:
    f.write(tflite_quant_model)

print(
    "[SUCCESS] Model trained, quantized to INT8, and exported to models/model.tflite"
)
