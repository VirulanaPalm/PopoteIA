"""Utilidad manual: lista las voces de síntesis instaladas en Windows (vía pyttsx3)."""

import pyttsx3

if __name__ == "__main__":
    engine = pyttsx3.init()
    voces = engine.getProperty("voices")

    print("\n--- VOCES INSTALADAS EN TU WINDOWS ---")
    for indice, voz in enumerate(voces):
        print(f"Número: {indice}")
        print(f"Nombre: {voz.name}")
        print("-" * 30)
