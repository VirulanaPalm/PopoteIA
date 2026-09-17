"""
Punto de entrada de POPOTE.

Arranca la interfaz visual (pantallita.CaraPopote) en el hilo principal,
y la lógica de escuchar / pensar / hablar en un hilo aparte, para que la
animación de la cara nunca se congele mientras Popote escucha o piensa.
"""

import threading
import tkinter as tk

import pythoncom

from pantallita import CaraPopote
from voice.listener import escuchar
from voice.speaker import decir
from voice.music import reproducir_musica, detener_musica
from brain.core import pensar

MENSAJE_BIENVENIDA = "Hola Agustín. Sistemas en línea e interfaz gráfica activada."
MENSAJE_DESPEDIDA = "Nos vemos hermano. Apagando sistemas. Aguante Boca."
MENSAJE_MUSICA_PAUSADA = "Música pausada, hermano."

COMANDOS_APAGADO = ("apagar sistema", "andate a dormir")

COMANDOS_DETENER_MUSICA = (
    "detener", "parar", "para la", "pará la",
    "apaga", "apagá", "silencio", "corta la", "cortá la",
)

# Solo dispara el modo música si el pedido arranca con uno de estos verbos,
# para no confundir un comentario cualquiera con una orden de reproducir algo.
VERBOS_PEDIR_MUSICA = (
    "poné", "ponete", "reproducir", "reproduce",
    "buscá", "busca", "quiero escuchar",
)


def _contiene_alguno(texto, palabras):
    return any(palabra in texto for palabra in palabras)


def _empieza_con_alguno(texto, prefijos):
    return any(texto.startswith(prefijo) for prefijo in prefijos)


def logica_ia(app):
    """Loop principal de Popote: escucha, interpreta el comando y responde."""
    pythoncom.CoInitialize()

    def hablar(texto):
        decir(texto, callback_inicio=app.iniciar_habla, callback_fin=app.detener_habla)

    hablar(MENSAJE_BIENVENIDA)

    while True:
        app.estado_escuchando()
        texto_usuario = escuchar()
        app.estado_normal()

        if not texto_usuario:
            continue

        texto_minus = texto_usuario.lower()

        # Comando de apagado
        if _contiene_alguno(texto_minus, COMANDOS_APAGADO):
            detener_musica()
            hablar(MENSAJE_DESPEDIDA)
            app.root.quit()
            break

        # 1. PRIORIDAD ABSOLUTA: frenar la música
        elif _contiene_alguno(texto_minus, COMANDOS_DETENER_MUSICA):
            detener_musica()
            hablar(MENSAJE_MUSICA_PAUSADA)

        # 2. MÚSICA: solo si la orden es clara y arranca con un verbo de pedido directo
        elif _empieza_con_alguno(texto_minus, VERBOS_PEDIR_MUSICA):
            app.estado_pensando()
            print("[POPOTE DJ LOCAL ACTIVADO]")
            respuesta_musica = reproducir_musica(texto_usuario)
            app.estado_normal()
            hablar(respuesta_musica)

        # 3. Charla normal con Groq (si no fue comando de música ni de frenado)
        else:
            app.estado_pensando()
            print("[POPOTE PENSANDO...]")
            respuesta_inteligente = pensar(texto_usuario)
            app.estado_normal()
            hablar(respuesta_inteligente)


def main():
    ventana = tk.Tk()
    app = CaraPopote(ventana)

    hilo_ia = threading.Thread(target=logica_ia, args=(app,), daemon=True)
    hilo_ia.start()

    ventana.mainloop()


if __name__ == "__main__":
    main()
