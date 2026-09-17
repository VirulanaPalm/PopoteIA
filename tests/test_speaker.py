"""
Prueba manual de un TTS alternativo con edge_tts (voz "es-AR-TomasNeural").

Nota: este NO es el TTS que usa main.py en producción (ese es
voice/speaker.py, vía PowerShell/System.Speech). Este script queda como
prueba/alternativa, sin integrar.
"""

import asyncio
import os

import edge_tts
from playsound import playsound

VOZ = "es-AR-TomasNeural"
ARCHIVO_AUDIO = "respuesta_popote.mp3"


async def _generar_audio(texto):
    """Función interna asíncrona para conectarse a Microsoft."""
    comunicacion = edge_tts.Communicate(texto, VOZ)
    await comunicacion.save(ARCHIVO_AUDIO)


def decir(texto):
    """Hace que POPOTE hable en voz alta e imprime en consola."""
    print(f"[POPOTE]: {texto}")

    asyncio.run(_generar_audio(texto))
    playsound(ARCHIVO_AUDIO)

    try:
        os.remove(ARCHIVO_AUDIO)
    except PermissionError:
        pass  # Por si Windows retiene el archivo un segundo de más
