"""Utilidad manual: lista los modelos disponibles en la cuenta de Groq configurada."""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
cliente = Groq(api_key=API_KEY)

if __name__ == "__main__":
    print("\n[BUSCANDO MODELOS DISPONIBLES EN GROQ...]")
    try:
        modelos = cliente.models.list()
        for m in modelos.data:
            print(f"- {m.id}")
    except Exception as e:
        print(f"Error: {e}")
    print("\n")
