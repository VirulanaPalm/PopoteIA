"""Prueba manual del cerebro conversacional (brain.core.pensar)."""

import os
import sys

# Le decimos a Python que mire en la carpeta anterior (la principal de POPOTE)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from brain.core import pensar

if __name__ == "__main__":
    print("\n[INICIANDO TEST DEL CEREBRO]")
    print("Agustín: ¿Quién sos y qué vas a ser en el futuro?")
    respuesta = pensar("¿Quién sos y qué vas a ser en el futuro?")
    print(f"\n[POPOTE RESPONDE]: {respuesta}\n")
