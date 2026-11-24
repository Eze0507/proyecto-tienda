from seguridad.api.utils.auditoria import obtener_contexto
from seguridad.application.services.auditoria import AuditoriaService
from seguridad.domain.enums import (
    AccionEvento,
    EntidadEvento,
    MotivoEvento,
    TipoEvento,
)
from seguridad.infrastructure.repositories.bitacora import DjangoBitacoraRepository


class AuditoriaPermisoMixin:
    auditoria_tipo_evento: TipoEvento | None = None
    auditoria_entidad: EntidadEvento | None = None
    auditoria_acciones: dict[str, AccionEvento] = {}
    auditoria_pk_kwarg: str | None = None

    def permission_denied(self, request, message=None, code=None):
        # Si is_authenticated es False, falló IsAuthenticated (401), no TienePermiso (403)
        if request.user and request.user.is_authenticated:
            accion = self.auditoria_acciones.get(request.method)
            if self.auditoria_tipo_evento and self.auditoria_entidad and accion:
                pk_val = (
                    self.kwargs.get(self.auditoria_pk_kwarg)
                    if self.auditoria_pk_kwarg
                    else None
                )

                auditoria = AuditoriaService(DjangoBitacoraRepository())
                auditoria.registrar_fallo(
                    tipo_evento=self.auditoria_tipo_evento,
                    accion=accion,
                    entidad=self.auditoria_entidad,
                    motivo=MotivoEvento.PERMISO_INSUFICIENTE,
                    registro_id=str(pk_val) if pk_val is not None else None,
                    contexto=obtener_contexto(request),
                )

        super().permission_denied(request, message=message, code=code)