import threading
import tkinter as tk
import pythoncom
import time
import difflib 
from pantallita import CaraPopote
from voice.listener import escuchar
from voice.speaker import decir, detener_habla 
from brain.core import pensar
from voice.music import reproducir_musica, detener_musica, atenuar_musica, normalizar_musica, cambiar_volumen

def logica_ia(app):
    pythoncom.CoInitialize()
    
    ultimo_texto_popote = ""
    durmiendo = False # Estado de siesta (reposo)
    
    def hablar(texto):
        nonlocal ultimo_texto_popote
        ultimo_texto_popote = texto.lower() 
        atenuar_musica()
        
        def al_terminar():
            app.detener_habla()
            normalizar_musica()
            
        decir(texto, callback_inicio=app.iniciar_habla, callback_fin=al_terminar)

    hablar("Popote en marcha!")
    
    hardware_ok = True 
    
    while True:
        atenuar_musica()
        app.estado_escuchando()
        texto_usuario = escuchar()
        app.estado_normal()
        normalizar_musica()
        
        if texto_usuario == "[ERROR_DISPOSITIVO]":
            if hardware_ok: 
                print("[SISTEMA ALERTA]: Sin conexión a audio o micrófono. Esperando hardware...")
                hardware_ok = False
            time.sleep(2) 
            continue
        else:
            if not hardware_ok:
                hardware_ok = True
                print("[SISTEMA ALERTA]: Conexión restablecida.")
                hablar("Conexión restablecida.")
        
        if texto_usuario:
            texto_minus = texto_usuario.lower().strip()
            
            # --- MODO REPOSO (SI ESTÁ DURMIENDO) ---
            if durmiendo:
                if any(palabra in texto_minus for palabra in ["popote", "despertate", "despierta", "hola"]):
                    durmiendo = False
                    hablar("¡Acá estoy, hermano! ¿Qué necesitás?")
                continue 
            
            # Filtro Anti-Eco
            similitud = difflib.SequenceMatcher(None, texto_minus, ultimo_texto_popote).ratio()
            if similitud > 0.45:
                continue 
            
            # INTERRUPCIÓN INSTANTÁNEA (Calla a Popote si empezaste a hablar)
            detener_habla() 
            
            # 1. Apagado total (Cierra la ventana de verdad)
            if any(frase in texto_minus for frase in ["apagar sistema", "cerrar programa"]):
                detener_musica()
                hablar("Nos vemos hermano. Apagando sistemas. Aguante Boca.")
                time.sleep(1.5)
                app.root.quit()
                break
                
            # 2. MODO REPOSO: Múltiples formas de mandarlo a dormir pero que siga escuchando
            elif any(palabra in texto_minus for palabra in ["dormi", "dormí", "dormite", "apagate", "apágate", "esperame", "espérame", "descansa"]):
                detener_musica()
                hablar("Me voy a dormir. Avisame si me necesitás.")
                durmiendo = True # Activa la siesta
                continue
                
            # 3. Frenar la música o callarlo sin que se vaya a dormir
            elif any(palabra in texto_minus for palabra in ["pará popote", "para popote", "silencio", "callate", "corta la"]):
                detener_musica()
                hablar("En pausa y escuchando.")
                continue
                
            # 4. Control de volumen
            elif "volumen" in texto_minus:
                app.estado_pensando()
                if "mitad" in texto_minus or "medio" in texto_minus:
                    respuesta = cambiar_volumen(0.5)
                elif "bajo" in texto_minus or "bajar" in texto_minus:
                    respuesta = cambiar_volumen(0.2)
                elif "alto" in texto_minus or "subir" in texto_minus or "cien" in texto_minus:
                    respuesta = cambiar_volumen(1.0)
                else:
                    try:
                        numeros = [int(s) for s in texto_minus.split() if s.isdigit()]
                        if numeros:
                            vol_final = max(0.0, min(1.0, numeros[0] / 100))
                            respuesta = cambiar_volumen(vol_final)
                        else:
                            respuesta = "No caché qué volumen querías, hermano."
                    except:
                        respuesta = "Tirame un número del 1 al 100 para el volumen."
                app.estado_normal()
                hablar(respuesta)

            # 5. Reproducir música
            elif any(verbo in texto_minus for verbo in ["poné", "ponete", "reproducir", "reproduce", "buscá", "busca", "quiero escuchar"]):
                app.estado_pensando() 
                print("[POPOTE DJ LOCAL ACTIVADO]")
                respuesta_musica = reproducir_musica(texto_usuario)
                app.estado_normal()
                hablar(respuesta_musica)
                
            # 6. Charla normal con Groq
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