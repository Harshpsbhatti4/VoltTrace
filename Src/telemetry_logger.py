import time
import serial

SERIAL_PORT = "/dev/ttyACM0"  # Update for your OS (e.g., 'COM3' on Windows)
BAUD_RATE = 115200


def run_logger():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"[VoltTrace] Listening on {SERIAL_PORT} at {BAUD_RATE} baud...")
        time.sleep(2)

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] {line}")
    except serial.SerialException as e:
        print(f"[ERROR] Serial connection failed: {e}")
    except KeyboardInterrupt:
        print("\n[VoltTrace] Logging terminated by user.")


if __name__ == "__main__":
    run_logger()
