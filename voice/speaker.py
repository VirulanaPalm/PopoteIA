import subprocess
import time
import threading

_proceso_voz = None

def _ejecutar_comando(comando, callback_inicio, callback_fin):
    global _proceso_voz
    try:
        _proceso_voz = subprocess.Popen(
            ["powershell", "-Command", comando], 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        time.sleep(0.2)
        if callback_inicio:
            callback_inicio()
        _proceso_voz.wait()
    except Exception:
        pass
    finally:
        if callback_fin:
            callback_fin()
        _proceso_voz = None

def decir(texto, callback_inicio=None, callback_fin=None):
    """Dice el texto en segundo plano."""
    global _proceso_voz
    
    detener_habla() 
    
    print(f"[POPOTE]: {texto}")
    texto_limpio = texto.replace('"', '').replace("'", "")
    
    comando = f"Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Rate = 2; $synth.Speak('{texto_limpio}');"
    
    hilo = threading.Thread(target=_ejecutar_comando, args=(comando, callback_inicio, callback_fin))
    hilo.daemon = True
    hilo.start()

def detener_habla():
    """Mata el proceso de voz de raíz con TaskKill de Windows. Interrupción instantánea."""
    global _proceso_voz
    if _proceso_voz:
        try:
            # Forzamos el cierre del proceso y todos sus subprocesos (/F /T)
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(_proceso_voz.pid)], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
        _proceso_voz = None