import speech_recognition as sr

def escuchar():
    r = sr.Recognizer()
    
    # Barrera fija en 500: Ignora la música al 15% y no se rompe con gritos de fondo.
    r.energy_threshold = 500 
    r.dynamic_energy_threshold = False 
    r.pause_threshold = 1.0 
    
    try:
        with sr.Microphone() as source:
            try:
                # Ya no usamos adjust_for_ambient_noise. Va directo a escuchar.
                audio = r.listen(source, timeout=3, phrase_time_limit=8)
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