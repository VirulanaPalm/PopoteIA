"""Prueba manual end-to-end de la voz edge_tts (genera y reproduce un audio de prueba)."""

import asyncio
import os

import edge_tts
from playsound import playsound

VOZ = "es-AR-TomasNeural"
TEXTO = "Hola Agustín. Ahora sí, esta voz suena muchísimo mejor. ¿Qué te parece? Vamos Boca."
ARCHIVO_AUDIO = "respuesta_temporal.mp3"


async def probar_voz():
    print("\n[POPOTE] Conectando con el servidor para generar la voz...")

    comunicacion = edge_tts.Communicate(TEXTO, VOZ)
    await comunicacion.save(ARCHIVO_AUDIO)

    print("[POPOTE] Reproduciendo audio...")
    playsound(ARCHIVO_AUDIO)

    try:
        os.remove(ARCHIVO_AUDIO)
    except PermissionError:
        pass  # Por si Windows retiene el archivo un segundo de más

    print("[POPOTE] Prueba terminada.\n")


if __name__ == "__main__":
    asyncio.run(probar_voz())
