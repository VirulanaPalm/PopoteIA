"""
Módulo de escucha (STT) de POPOTE.

Usa el micrófono por defecto del sistema y el reconocimiento de voz
gratuito de Google, configurado para español rioplatense.
"""

import speech_recognition as sr

# 0.7 es el punto dulce: deja hacer micropausas sin cortar,
# pero responde rápido cuando termina la frase posta.
PAUSE_THRESHOLD = 0.7
NON_SPEAKING_DURATION = 0.5

TIMEOUT_SEGUNDOS = 5
# Un poco holgado por si Agus le quiere dar una orden larga.
PHRASE_TIME_LIMIT_SEGUNDOS = 15

IDIOMA = "es-AR"


def escuchar() -> str:
    """Escucha por el micrófono y devuelve el texto reconocido (o "" si no entendió nada)."""
    reconocedor = sr.Recognizer()
    reconocedor.pause_threshold = PAUSE_THRESHOLD
    reconocedor.non_speaking_duration = NON_SPEAKING_DURATION

    with sr.Microphone() as source:
        print("\n[POPOTE] Escuchando...")
        try:
            audio = reconocedor.listen(
                source,
                timeout=TIMEOUT_SEGUNDOS,
                phrase_time_limit=PHRASE_TIME_LIMIT_SEGUNDOS,
            )
            texto = reconocedor.recognize_google(audio, language=IDIOMA)
            print(f"[USUARIO]: {texto}")
            return texto
        except Exception:
            # Timeout, silencio o audio que no se entendió: Popote no escuchó nada útil.
            return ""
