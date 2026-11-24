from datetime import datetime, timezone
from typing import Any
from uuid import UUID
from dataclasses import dataclass

from seguridad.application.ports.bitacora import (
    BitacoraRepositoryPort,
    RegistroAuditoriaDTO,
)

from seguridad.domain.enums import (
    TipoEvento,
    AccionEvento,
    ResultadoEvento,
    MotivoEvento,
    OrigenEvento,
    EntidadEvento,
)

@dataclass(frozen=True)
class ContextoAuditoria:
    usuario_id: int | None = None
    usuario_nombre: str | None = None
    sucursal_id: int | None = None
    sucursal_nombre: str | None = None
    ip: str | None = None
    origen: OrigenEvento = OrigenEvento.WEB

class AuditoriaService:
    def __init__(self, bitacora_repo: BitacoraRepositoryPort):
        self.bitacora_repo = bitacora_repo
    
    def registrar_exito(
        self,
        *,
        tipo_evento: TipoEvento,
        accion: AccionEvento,
        motivo: MotivoEvento | None = None,
        entidad: EntidadEvento,
        origen: OrigenEvento = OrigenEvento.WEB,
        datos_anteriores: dict[str, Any] | None = None,
        datos_nuevos: dict[str, Any] | None = None,
        usuario_id: int | None = None,
        usuario_nombre: str | None = None, 
        sucursal_id: int | None = None,
        sucursal_nombre: str | None = None,
        registro_id: str | None = None,
        ip: str | None = None,
        occurred_at: datetime | None = None,
        evento_id: UUID | None = None,
    ) -> None:
        evento = RegistroAuditoriaDTO(
            tipo_evento=tipo_evento.value,
            accion=accion.value,
            resultado=ResultadoEvento.EXITOSO.value,
            motivo=motivo.value if motivo else None,
            origen=origen.value,
            entidad=entidad.value,
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            usuario_id=usuario_id,
            usuario_nombre=usuario_nombre,
            sucursal_id=sucursal_id,
            sucursal_nombre=sucursal_nombre,
            registro_id=registro_id,
            ip=ip,
            occurred_at=occurred_at or datetime.now(timezone.utc),
            id=evento_id,
        )
        self.bitacora_repo.guardar(evento)
    
    def registrar_fallo(
        self,
        *,
        tipo_evento: TipoEvento,
        accion: AccionEvento,
        motivo: MotivoEvento | None = None,
        usuario_id: int | None = None,
        usuario_nombre: str | None = None,
        sucursal_id: int | None = None,
        sucursal_nombre: str | None = None,
        entidad: EntidadEvento,
        registro_id: str | None = None,
        origen: OrigenEvento = OrigenEvento.WEB,
        ip: str | None = None,
        occurred_at: datetime | None = None,
        evento_id: UUID | None = None,
    ) -> None:
        evento = RegistroAuditoriaDTO(
            tipo_evento=tipo_evento.value,
            accion=accion.value,
            motivo=motivo.value if motivo else None,
            resultado=ResultadoEvento.FALLIDO.value,
            usuario_id=usuario_id,
            usuario_nombre=usuario_nombre,
            sucursal_id=sucursal_id,
            sucursal_nombre=sucursal_nombre,
            entidad=entidad.value,
            registro_id=registro_id,
            origen=origen.value,
            ip=ip,
            occurred_at=occurred_at or datetime.now(timezone.utc),
            id=evento_id,
        )
        self.bitacora_repo.guardar(evento)