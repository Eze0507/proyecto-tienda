from datetime import datetime, timezone
from typing import Any
from uuid import UUID
from dataclasses import dataclass
import logging

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

logger = logging.getLogger(__name__)

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

    def _registrar(
        self,
        *,
        tipo_evento: TipoEvento,
        accion: AccionEvento,
        resultado: ResultadoEvento,
        entidad: EntidadEvento,
        motivo: MotivoEvento | None = None,
        registro_id: str | None = None,
        datos_anteriores: dict[str, Any] | None = None,
        datos_nuevos: dict[str, Any] | None = None,
        contexto: ContextoAuditoria | None = None,
        occurred_at: datetime | None = None,
        evento_id: UUID | None = None,
    ) -> None:
        ctx = contexto or ContextoAuditoria()

        evento = RegistroAuditoriaDTO(
            tipo_evento=tipo_evento.value,
            accion=accion.value,
            resultado=resultado.value,
            motivo=motivo.value if motivo else None,
            origen=ctx.origen.value,
            entidad=entidad.value,
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            usuario_id=ctx.usuario_id,
            usuario_nombre=ctx.usuario_nombre,
            sucursal_id=ctx.sucursal_id,
            sucursal_nombre=ctx.sucursal_nombre,
            registro_id=registro_id,
            ip=ctx.ip,
            occurred_at=occurred_at or datetime.now(timezone.utc),
            id=evento_id,
        )
        self.bitacora_repo.guardar(evento)

    def registrar_exito(
        self,
        *,
        tipo_evento: TipoEvento,
        accion: AccionEvento,
        entidad: EntidadEvento,
        registro_id: str | None = None,
        datos_anteriores: dict[str, Any] | None = None,
        datos_nuevos: dict[str, Any] | None = None,
        contexto: ContextoAuditoria | None = None,
        occurred_at: datetime | None = None,
        evento_id: UUID | None = None,
    ) -> None:
        self._registrar(
            tipo_evento=tipo_evento,
            accion=accion,
            resultado=ResultadoEvento.EXITOSO,
            entidad=entidad,
            registro_id=registro_id,
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            contexto=contexto,
            occurred_at=occurred_at,
            evento_id=evento_id,
        )

    def registrar_fallo(
        self,
        *,
        tipo_evento: TipoEvento,
        accion: AccionEvento,
        entidad: EntidadEvento,
        motivo: MotivoEvento | None = None,
        registro_id: str | None = None,
        contexto: ContextoAuditoria | None = None,
        occurred_at: datetime | None = None,
        evento_id: UUID | None = None,
    ) -> None:
        try:
            self._registrar(
                tipo_evento=tipo_evento,
                accion=accion,
                resultado=ResultadoEvento.FALLIDO,
                entidad=entidad,
                motivo=motivo,
                registro_id=registro_id,
                contexto=contexto,
                occurred_at=occurred_at,
                evento_id=evento_id,
            )
        except Exception:
            logger.exception("No se pudo registrar el fallo en la bitacora")