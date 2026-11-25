from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

@dataclass(frozen=True)
class RegistroAuditoriaDTO:
    tipo_evento: str
    accion: str
    resultado: str
    entidad: str
    origen: str
    occurred_at: datetime
    motivo: str | None = None
    usuario_id: int | None = None
    usuario_nombre: str | None = None
    sucursal_id: int | None = None
    sucursal_nombre: str | None = None
    registro_id: str | None = None
    ip: str | None = None
    datos_anteriores: dict[str, Any] | None = None
    datos_nuevos: dict[str, Any] | None = None
    id: UUID | None = None

class BitacoraRepositoryPort(ABC):
    
    @abstractmethod
    def guardar(self, registro: RegistroAuditoriaDTO) -> None:
        pass