import speech_recognition as sr

def escuchar():
    r = sr.Recognizer()
    
    try:
        # Intentamos abrir el micrófono...
        with sr.Microphone() as source:
            r.pause_threshold = 0.7
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=10)
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
        # ¡Magia! Si cae acá es porque no hay micrófono conectado
        return "[ERROR_DISPOSITIVO]"