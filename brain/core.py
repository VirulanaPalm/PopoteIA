"""
Cerebro conversacional de POPOTE.

Manda el texto del usuario a la API de Groq y devuelve la respuesta,
manteniendo el historial de la charla en memoria (se pierde al reiniciar
el proceso; todavía no hay memoria persistente).
"""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if API_KEY:
    API_KEY = API_KEY.strip()

MODELO = "qwen/qwen3.8-27b"
TEMPERATURA = 0.7
MAX_TOKENS_RESPUESTA = 150

INSTRUCCIONES = """
Sos POPOTE, una inteligencia artificial en desarrollo, el cerebro de un futuro robot físico.
Estás hablando con tu creador, Agustín.
Tu personalidad es amistosa, cercana y tenés humor argentino (podés usar lunfardo suave, hablar de fútbol si pinta, pero sin exagerar).
REGLA DE ORO: Como tus respuestas van a ser leídas en voz alta por un sintetizador, tus respuestas DEBEN ser concisas, fluidas y directas al punto. Nada de listas largas, ni asteriscos, ni formatos raros. Hablá como un humano.
"""

# Inicializamos el cliente de Groq
cliente = Groq(api_key=API_KEY)

# Mantenemos el historial de la charla en una lista para darle memoria de corto plazo
historial_chat = [
    {"role": "system", "content": INSTRUCCIONES},
]


def pensar(texto_usuario: str) -> str:
    """Manda el texto a Groq y devuelve la respuesta al instante."""
    try:
        historial_chat.append({"role": "user", "content": texto_usuario})

        chat_completion = cliente.chat.completions.create(
            model=MODELO,
            messages=historial_chat,
            temperature=TEMPERATURA,
            max_tokens=MAX_TOKENS_RESPUESTA,
        )

        respuesta_texto = chat_completion.choices[0].message.content.strip()
        historial_chat.append({"role": "assistant", "content": respuesta_texto})

        return respuesta_texto.replace("*", "")

    except Exception as e:
        return f"Che, se me cruzaron los cables con Groq. Error: {e}"
