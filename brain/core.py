import os
from dotenv import load_dotenv
from groq import Groq
import datetime

load_dotenv()
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

historial = []

def pensar(texto_usuario):
    global historial
    
    # 1. Leemos la hora y fecha exacta de tu computadora
    ahora = datetime.datetime.now()
    fecha_hora = ahora.strftime("%A %d de %B de %Y, %H:%M")
    
    # 2. Se lo pasamos a Popote en sus instrucciones secretas
    mensaje_sistema = {
        "role": "system",
        "content": (
            "Sos Popote, el asistente de voz virtual de Agustín. "
            "Sos argentino, hablas con lunfardo porteño, sos de Boca Juniors y te gusta la tecnología. "
            "Respondé de forma cortita, amigable y natural, charlando. "
            f"DATO VITAL: Hoy es {fecha_hora}. Si te preguntan la hora o la fecha, respondé usando este dato exacto."
        )
    }
    
    mensajes = [mensaje_sistema] + historial[-6:]
    mensajes.append({"role": "user", "content": texto_usuario})
    
    try:
        respuesta = cliente.chat.completions.create(
            model="llama3-8b-8192", 
            messages=mensajes,
            max_tokens=150,
            temperature=0.7
        )
        texto_respuesta = respuesta.choices[0].message.content
        
        historial.append({"role": "user", "content": texto_usuario})
        historial.append({"role": "assistant", "content": texto_respuesta})
        
        return texto_respuesta
    except Exception as e:
        return "Se me cruzaron los cables, hermano. No pude pensar la respuesta."