import serial
import time

print("================================")
print("     POPOTE'S - CEREBRO")
print("================================")
print("Conectando con ESP32...")

esp32 = serial.Serial("COM5", 115200, timeout=1)

time.sleep(2)

print("ESP32 conectado.")
print("Popote's está escuchando...")
print()

while True:
    linea = esp32.readline().decode("utf-8", errors="ignore").strip()

    if not linea:
        continue

    if ">>> POPOTE'S ESCUCHA" in linea:
        print("🎤 Popote's: TE ESCUCHO")

    elif "Silencio" in linea:
        print("😴 Popote's: ...")

    else:
        print(f"[ESP32] {linea}")