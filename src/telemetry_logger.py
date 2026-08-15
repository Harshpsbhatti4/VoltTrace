import serial
import serial.tools.list_ports
import time
import os
import sys

BAUD_RATE = 115200
OUTPUT_FILE = os.path.join("data", "live_telemetry.csv")

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description or "USB" in port.description:
            return port.device
    return ports[0].device if ports else None

def main():
    os.makedirs("data", exist_ok=True)
    port = find_arduino_port()
    if not port:
        print("[ERROR] No active serial device detected. Please connect your board.")
        sys.exit(1)

    print(f"[VoltTrace Telemetry Logger] Connecting to {port} @ {BAUD_RATE} baud...")
    
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=2)
        time.sleep(2) # Allow board reboot on connection
        print(f"[CONNECTED] Logging telemetry to {OUTPUT_FILE} (Press Ctrl+C to stop)")

        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            while True:
                if ser.in_waiting > 0:
                    raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
                    if raw_line and not raw_line.startswith("["):
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        entry = f"{timestamp},{raw_line}"
                        print(f"[{timestamp}] {raw_line}")
                        f.write(entry + "\n")
                        f.flush()
    except KeyboardInterrupt:
        print("\n[INFO] Logging terminated by user.")
    except Exception as e:
        print(f"\n[ERROR] Serial communication failed: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
