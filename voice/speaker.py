"""
Módulo de habla (TTS) de POPOTE.

Sintetiza voz con System.Speech de Windows a través de PowerShell, para
no depender de servicios externos ni de conexión a internet.
"""

import subprocess
import time

VELOCIDAD_VOZ = 2
PAUSA_SINCRONIZACION_BOCA_SEGUNDOS = 0.25


def decir(texto: str, callback_inicio=None, callback_fin=None) -> None:
    """Hace hablar a Popote y dispara los callbacks para animar la boca."""
    print(f"[POPOTE]: {texto}")

    texto_limpio = texto.replace('"', "").replace("'", "")

    comando = f"""
    Add-Type -AssemblyName System.Speech;
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $synth.Rate = {VELOCIDAD_VOZ};
    $synth.Speak('{texto_limpio}');
    """

    proceso = subprocess.Popen(
        ["powershell", "-Command", comando],
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    # Pausa preventiva para sincronizar la boca con el primer sonido
    time.sleep(PAUSA_SINCRONIZACION_BOCA_SEGUNDOS)

    if callback_inicio:
        callback_inicio()

    # Esperamos a que termine de hablar al 100%
    proceso.wait()

    if callback_fin:
        callback_fin()
