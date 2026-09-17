import subprocess
import time

def decir(texto, callback_inicio=None, callback_fin=None):
    print(f"[POPOTE]: {texto}")
    texto_limpio = texto.replace('"', '').replace("'", "")
    
    comando = f"""
    Add-Type -AssemblyName System.Speech;
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $synth.Rate = 2; 
    $synth.Speak('{texto_limpio}');
    """
    
    try:
        # Intentamos reproducir el sonido
        proceso = subprocess.Popen(
            ["powershell", "-Command", comando], 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        time.sleep(0.25)
        
        if callback_inicio:
            callback_inicio()
            
        proceso.wait() 
    except Exception:
        # Falla silenciosa: si no hay parlantes, simplemente sigue el programa
        pass 
        
    if callback_fin:
        callback_fin()