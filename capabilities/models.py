"""
Modelo de datos de una Capability dentro del Capability Registry de POPOTE.

Ver documento maestro del proyecto: cada capacidad tiene nombre, id,
versión, descripción, estado, dependencias, archivos, riesgo, autor,
fecha de creación y si fue aprobada por Agus.
"""

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import List, Optional

ESTADOS_VALIDOS = (
    "enabled", "disabled", "development",
    "testing", "failed", "deprecated", "deleted",
)


@dataclass
class Capability:
    id: str
    nombre: str
    descripcion: str
    version: str = "1.0.0"
    estado: str = "enabled"
    dependencias: List[str] = field(default_factory=list)
    archivos: List[str] = field(default_factory=list)
    riesgo: str = "bajo"  # bajo | medio | alto
    autor: str = "agus"
    fecha_creacion: str = field(default_factory=lambda: date.today().isoformat())
    version_anterior: Optional[str] = None
    aprobado_por_agus: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Capability":
        return cls(**data)
