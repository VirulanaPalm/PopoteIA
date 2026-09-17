"""Prueba manual del micrófono: graba 5 segundos y transcribe con Google STT."""

import sounddevice as sd
import speech_recognition as sr

FRECUENCIA_HZ = 16000
SEGUNDOS = 5

if __name__ == "__main__":
    print("\n[POPOTE] Preparando oídos...")
    print(f"[POPOTE] Hablá ahora (te escucho por {SEGUNDOS} segundos)...")

    grabacion = sd.rec(int(SEGUNDOS * FRECUENCIA_HZ), samplerate=FRECUENCIA_HZ, channels=1, dtype="int16")
    sd.wait()

    print("[POPOTE] Procesando lo que dijiste...")

    audio_bytes = grabacion.tobytes()
    audio_data = sr.AudioData(audio_bytes, FRECUENCIA_HZ, 2)  # 2 bytes = 16 bits

    recognizer = sr.Recognizer()

    try:
        texto = recognizer.recognize_google(audio_data, language="es-AR")
        print(f"\n[POPOTE ESCUCHÓ]: {texto}\n")
    except sr.UnknownValueError:
        print("\n[POPOTE ERROR]: Escuché ruido pero no entendí ninguna palabra.\n")
    except sr.RequestError as e:
        print(f"\n[POPOTE ERROR]: No me pude conectar al servicio de Google. {e}\n")
    except Exception as e:
        print(f"\n[POPOTE ERROR RARO]: Pasó algo inesperado: {e}\n")
