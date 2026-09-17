"""
Capability Registry de POPOTE — Fase 1 del Self Development Engine.

Es el inventario oficial de las capacidades del sistema: qué existe, en
qué estado está, de qué depende y qué archivos la componen. Se guarda en
config/capabilities.json.

IMPORTANTE (Fase 1): este registro es puramente informativo/consultivo.
No modifica ni condiciona en nada el comportamiento de main.py ni de
ningún módulo existente — es una capa aditiva por encima de lo que ya
funciona. Las fases siguientes (sandbox, tests, voz) son las que le dan
uso activo a este inventario.
"""

import json
import os
from typing import Dict, List, Optional

try:
    from capabilities.models import Capability
except ImportError:
    # Permite ejecutar este archivo tanto con `python capabilities/registry.py`
    # (ejecución directa) como con `python -m capabilities.registry` (como paquete).
    from models import Capability

RUTA_REGISTRY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config", "capabilities.json",
)


class CapabilityRegistry:
    def __init__(self, ruta: str = RUTA_REGISTRY):
        self._ruta = ruta
        self._capacidades: Dict[str, Capability] = {}
        self._cargar()

    def _cargar(self) -> None:
        if not os.path.exists(self._ruta):
            self._capacidades = {}
            return
        with open(self._ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._capacidades = {c["id"]: Capability.from_dict(c) for c in data}

    def _guardar(self) -> None:
        os.makedirs(os.path.dirname(self._ruta), exist_ok=True)
        with open(self._ruta, "w", encoding="utf-8") as f:
            json.dump(
                [c.to_dict() for c in self._capacidades.values()],
                f, ensure_ascii=False, indent=2,
            )

    def registrar(self, capacidad: Capability, sobrescribir: bool = False) -> None:
        """Agrega una capacidad nueva al registro (o la actualiza si sobrescribir=True)."""
        if capacidad.id in self._capacidades and not sobrescribir:
            return
        self._capacidades[capacidad.id] = capacidad
        self._guardar()

    def obtener(self, capacidad_id: str) -> Optional[Capability]:
        return self._capacidades.get(capacidad_id)

    def listar(self, estado: Optional[str] = None) -> List[Capability]:
        capacidades = list(self._capacidades.values())
        if estado:
            capacidades = [c for c in capacidades if c.estado == estado]
        return capacidades

    def cambiar_estado(self, capacidad_id: str, nuevo_estado: str) -> bool:
        capacidad = self._capacidades.get(capacidad_id)
        if not capacidad:
            return False
        capacidad.estado = nuevo_estado
        self._guardar()
        return True


def registro_inicial() -> CapabilityRegistry:
    """Crea (si no existe) el registro con las 5 capacidades ya presentes en el proyecto."""
    registry = CapabilityRegistry()

    capacidades_core = [
        Capability(
            id="brain_core",
            nombre="Cerebro conversacional",
            descripcion="Conversación general vía Groq (brain/core.py).",
            archivos=["brain/core.py"],
            riesgo="medio",
        ),
        Capability(
            id="voice_listener",
            nombre="Escucha (STT)",
            descripcion="Reconocimiento de voz en español rioplatense (voice/listener.py).",
            archivos=["voice/listener.py"],
            riesgo="bajo",
        ),
        Capability(
            id="voice_speaker",
            nombre="Habla (TTS)",
            descripcion="Síntesis de voz vía PowerShell/System.Speech (voice/speaker.py).",
            archivos=["voice/speaker.py"],
            riesgo="bajo",
        ),
        Capability(
            id="voice_music",
            nombre="Música (DJ local)",
            descripcion="Búsqueda y reproducción local de audio de YouTube (voice/music.py).",
            archivos=["voice/music.py"],
            riesgo="medio",
            dependencias=["yt-dlp", "ffmpeg", "ffplay"],
        ),
        Capability(
            id="cara_visual",
            nombre="Interfaz visual (cara)",
            descripcion="Animación de ojos, boca y brillo según estado (pantallita.py).",
            archivos=["pantallita.py"],
            riesgo="bajo",
        ),
    ]

    for capacidad in capacidades_core:
        registry.registrar(capacidad, sobrescribir=False)

    return registry


if __name__ == "__main__":
    # Ejecutar este archivo directamente crea/actualiza config/capabilities.json
    # con el inventario inicial. No importa ni toca ningún otro módulo del proyecto.
    r = registro_inicial()
    print(f"Capability Registry listo con {len(r.listar())} capacidades en {RUTA_REGISTRY}")
    for c in r.listar():
        print(f"  [{c.estado.upper()}] {c.nombre} (id={c.id}, riesgo={c.riesgo})")
