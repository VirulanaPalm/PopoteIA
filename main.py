import threading
import tkinter as tk
import pythoncom
import time
import difflib 
import re 
from pantallita import CaraPopote
from voice.listener import escuchar
from voice.speaker import decir, detener_habla 
from brain.core import pensar
from voice.music import reproducir_musica, detener_musica, atenuar_musica, normalizar_musica, cambiar_volumen

def logica_ia(app):
    pythoncom.CoInitialize()
    
    ultimo_texto_popote = ""
    durmiendo = False
    
    def hablar(texto):
        nonlocal ultimo_texto_popote
        ultimo_texto_popote = texto.lower() 
        
        def al_terminar():
            app.detener_habla()
            normalizar_musica() 
            
        decir(texto, callback_inicio=app.iniciar_habla, callback_fin=al_terminar)

    hablar("Popote en marcha!")
    hardware_ok = True 
    
    while True:
        app.estado_escuchando()
        texto_usuario = escuchar()
        app.estado_normal()
        
        if not texto_usuario or texto_usuario == "[ERROR_DISPOSITIVO]":
            if texto_usuario == "[ERROR_DISPOSITIVO]":
                if hardware_ok: 
                    print("[SISTEMA ALERTA]: Sin conexión a audio o micrófono. Esperando hardware...")
                    hardware_ok = False
                time.sleep(2) 
            continue
            
        if not hardware_ok:
            hardware_ok = True
            print("[SISTEMA ALERTA]: Conexión restablecida.")
            hablar("Conexión restablecida.")
        
        texto_minus = texto_usuario.lower().strip()
        
        if durmiendo:
            if any(palabra in texto_minus for palabra in ["popote", "despertate", "despierta", "hola"]):
                durmiendo = False
                hablar("¡Acá estoy, hermano! ¿Qué necesitás?")
            continue 
        
        # FILTRO ANTI-ECO CORREGIDO A 85% (antes estaba en 45% y te bloqueaba comandos válidos)
        similitud = difflib.SequenceMatcher(None, texto_minus, ultimo_texto_popote).ratio()
        if similitud > 0.85:
            continue 
        
        atenuar_musica()
        detener_habla() 
        texto_comando = texto_minus.replace("popote", "").replace("che", "").replace("puedes", "").replace("podés", "").strip()
        
        if any(frase in texto_minus for frase in ["apagar sistema", "cerrar programa"]):
            detener_musica()
            hablar("Nos vemos hermano. Apagando sistemas. Aguante Boca.")
            time.sleep(1.5)
            app.root.quit()
            break
            
        elif any(palabra in texto_minus for palabra in ["dormi", "dormí", "dormite", "apagate", "apágate", "esperame", "espérame", "descansa"]):
            detener_musica()
            hablar("Me voy a dormir. Avisame si me necesitás.")
            durmiendo = True 
            continue
            
        elif any(palabra in texto_minus for palabra in ["pausa", "pausá", "pausar", "detener", "parar", "frená", "frena", "stop", "silencio", "corta la", "cortá la", "para la", "pará la"]):
            detener_musica()
            hablar("Música pausada.")
            continue

        elif any(palabra in texto_minus for palabra in ["volumen", "volúmen", "subí", "subi", "sube", "subilo", "bajá", "baja", "bajalo", "mas fuerte", "más fuerte", "mas despacio", "más despacio", "mas bajo", "más bajo"]):
            app.estado_pensando()
            
            numeros = [int(s) for s in re.findall(r'\d+', texto_minus)]
            
            if numeros:
                vol_final = max(0.0, min(1.0, numeros[0] / 100))
                respuesta = cambiar_volumen(vol_final)
            elif any(p in texto_minus for p in ["mitad", "medio", "cincuenta"]):
                respuesta = cambiar_volumen(0.5)
            elif any(p in texto_minus for p in ["bajo", "bajale", "bajar", "despacio", "baja", "bajá", "bajalo"]):
                respuesta = cambiar_volumen(0.2)
            elif any(p in texto_minus for p in ["alto", "fuerte", "cien", "subile", "subir", "subi", "subí", "sube", "subilo"]):
                respuesta = cambiar_volumen(1.0)
            else:
                respuesta = "No caché a qué volumen. Decime un número."
                
            app.estado_normal()
            hablar(respuesta)

        elif any(verbo in texto_comando for verbo in ["cambiá", "cambia", "siguiente", "pasá", "pasa", "otro tema", "otra canción", "otra cancion", "pasala", "saltealo"]):
            app.estado_pensando()
            respuesta_musica = reproducir_musica("") 
            app.estado_normal()
            hablar(respuesta_musica)

        elif any(verbo in texto_comando for verbo in ["poné", "pone", "ponete", "poneme", "reproducir", "reproduce", "reproducí", "reproduci", "producir", "producí", "buscá", "busca", "quiero escuchar", "dale play", "toca", "tocá", "mandale", "mandá"]):
            app.estado_pensando() 
            print("[POPOTE DJ LOCAL ACTIVADO]")
            respuesta_musica = reproducir_musica(texto_usuario)
            app.estado_normal()
            hablar(respuesta_musica)
            
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