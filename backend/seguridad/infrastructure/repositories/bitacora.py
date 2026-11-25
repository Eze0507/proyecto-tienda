from seguridad.application.ports.bitacora import (
    BitacoraRepositoryPort,
    RegistroAuditoriaDTO
)
from seguridad.models import Bitacora

class DjangoBitacoraRepository(BitacoraRepositoryPort):
    def guardar(self, registro: RegistroAuditoriaDTO) -> None:
        datos = {
            "tipo_evento": registro.tipo_evento,
            "accion": registro.accion,
            "resultado": registro.resultado,
            "entidad": registro.entidad,
            "origen": registro.origen,
            "occurred_at": registro.occurred_at,
            "motivo": registro.motivo,
            "usuario_id": registro.usuario_id,
            "usuario_nombre": registro.usuario_nombre,
            "sucursal_id": registro.sucursal_id,
            "sucursal_nombre": registro.sucursal_nombre,
            "registro_id": registro.registro_id,
            "ip": registro.ip,
            "datos_anteriores": registro.datos_anteriores,
            "datos_nuevos": registro.datos_nuevos,
        }
        if registro.id is not None:
            datos["id"] = registro.id
        
        Bitacora.objects.create(**datos)