import speech_recognition as sr

def escuchar():
    r = sr.Recognizer()
    
    # Sensibilidad base (300 es ideal para una habitación normal)
    r.energy_threshold = 300 
    r.dynamic_energy_threshold = True 
    r.pause_threshold = 1.2
    r.non_speaking_duration = 0.4
    
    try:
        with sr.Microphone() as source:
            # ELIMINAMOS el adjust_for_ambient_noise. 
            # Ahora empieza a grabar INMEDIATAMENTE sin comerse tus primeras palabras.
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=15)
                texto = r.recognize_google(audio, language='es-AR')
                print(f"[USUARIO]: {texto}")
                return texto
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                print("[POPOTE]: Sin conexión a internet.")
                return ""
                
    except Exception as e:
        return "[ERROR_DISPOSITIVO]"