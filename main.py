import threading
import tkinter as tk
import pythoncom
import time
from pantallita import CaraPopote
from voice.listener import escuchar
from voice.speaker import decir
from brain.core import pensar
from voice.music import reproducir_musica, detener_musica, atenuar_musica, normalizar_musica

def logica_ia(app):
    pythoncom.CoInitialize()
    
    def hablar(texto):
        atenuar_musica()
        decir(texto, callback_inicio=app.iniciar_habla, callback_fin=app.detener_habla)
        normalizar_musica()

    hablar("Hola Agustín. Sistemas en línea e interfaz gráfica activada.")
    
    # Memoria de estado del hardware
    hardware_ok = True 
    
    while True:
        atenuar_musica()
        app.estado_escuchando()
        texto_usuario = escuchar()
        app.estado_normal()
        normalizar_musica()
        
        # --- CONTROL INTELIGENTE DE HARDWARE ---
        if texto_usuario == "[ERROR_DISPOSITIVO]":
            if hardware_ok: 
                # Solo imprime el error la primera vez que se cae, para no hacer spam
                print("[SISTEMA ALERTA]: Sin conexión a audio o micrófono. Esperando hardware...")
                hardware_ok = False
            time.sleep(2) # Espera 2 segundos y vuelve a escanear
            continue
        else:
            # Si logró leer algo (texto o silencio) pero estaba caído, ¡significa que volvió!
            if not hardware_ok:
                hardware_ok = True
                print("[SISTEMA ALERTA]: Conexión restablecida.")
                hablar("Conexión restablecida. Ya puedo hablar y escuchar de nuevo.")
        
        # --- PROCESAMIENTO DE COMANDOS ---
        if texto_usuario:
            texto_minus = texto_usuario.lower()
            
            # Comando de apagado
            if "apagar sistema" in texto_minus or "andate a dormir" in texto_minus:
                detener_musica()
                hablar("Nos vemos hermano. Apagando sistemas. Aguante Boca.")
                app.root.quit()
                break
                
            # 1. Frenar la música
            elif any(palabra in texto_minus for palabra in ["detener", "parar", "para la", "pará la", "apaga", "apagá", "silencio", "corta la", "cortá la"]):
                detener_musica()
                hablar("Música pausada, hermano.")
                
            # 2. Reproducir música
            elif any(texto_minus.startswith(verbo) for verbo in ["poné", "ponete", "reproducir", "reproduce", "buscá", "busca", "quiero escuchar"]):
                app.estado_pensando() 
                print("[POPOTE DJ LOCAL ACTIVADO]")
                respuesta_musica = reproducir_musica(texto_usuario)
                app.estado_normal()
                hablar(respuesta_musica)
                
            # 3. Charla normal con Groq
            else:
                app.estado_pensando() 
                print("[POPOTE PENSANDO...]")
                respuesta_inteligente = pensar(texto_usuario)
                app.estado_normal()
                hablar(respuesta_inteligente)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = CaraPopote(ventana)
    
    hilo_ia = threading.Thread(target=logica_ia, args=(app,))
    hilo_ia.daemon = True 
    hilo_ia.start()
    
    ventana.mainloop()