"""Casos de uso que coordinan el dominio mediante los puertos."""
from seguridad.application.ports.roles import RolRepositoryPort
from seguridad.application.validators import validar_permisos
from seguridad.domain.exceptions import (
    RolNoEncontrado,
    RolYaExiste,
    RolConUsuariosAsignados
)
from seguridad.application.services.auditoria import AuditoriaService
from seguridad.application.services.auditoria import ContextoAuditoria
from seguridad.domain.enums import TipoEvento, AccionEvento, EntidadEvento, MotivoEvento

class ListarRoles:
    def __init__(self, rol_repository: RolRepositoryPort):
        self.rol_repository = rol_repository
    
    def ejecutar(self):
        return self.rol_repository.Listar()

class ObtenerDetalleRol:
    def __init__(self, rol_repository: RolRepositoryPort):
        self.rol_repository = rol_repository
    
    def ejecutar(self, id_rol: int):
        rol = self.rol_repository.obtener_detalle(id_rol)
        
        if rol  is None:
            raise RolNoEncontrado(
                "El rol solicitado no existe"
            )
        
        return rol

class CrearRol:
    def __init__(self, rol_repository: RolRepositoryPort, auditoria: AuditoriaService):
        self.rol_repository = rol_repository
        self.auditoria = auditoria
    
    def ejecutar(
        self,
        nombre: str,
        permission_ids: list[int] | None,
        contexto: ContextoAuditoria | None = None
    ):
        if self.rol_repository.existe_por_nombre(nombre):
            raise RolYaExiste(
                "Ya existe un rol con ese nombre."
            )
        
        if permission_ids is not None:
            permission_ids = validar_permisos(
                permission_ids,
                self.rol_repository
            )
        
        rol = self.rol_repository.crear_con_permisos(
            nombre=nombre,
            permission_ids=permission_ids
        )
        
        self.auditoria.registrar_exito(
            tipo_evento=TipoEvento.USUARIOS,
            accion=AccionEvento.REGISTRAR_ROL,
            entidad=EntidadEvento.ROLES,
            registro_id=str(rol.id),
            datos_nuevos={
                "nombre": rol.name,
                "permission_ids": permission_ids or [],
            },
            contexto=contexto,
        )
        
        return rol

class ActualizarRol:
    def __init__(self, rol_repository: RolRepositoryPort, auditoria: AuditoriaService):
        self.rol_repository = rol_repository
        self.auditoria = auditoria
    
    def ejecutar(
        self, id_rol: int, 
        nombre: str | None = None, 
        permission_ids: list[int] | None = None,
        contexto: ContextoAuditoria | None = None,
    ):
        rol = self.rol_repository.obtener_por_id(id_rol)
        
        nombre_cambio = nombre is not None and nombre != rol.name
        
        if nombre_cambio and self.rol_repository.existe_por_nombre(
                nombre,
                id_rol
        ):
            raise RolYaExiste(
                "Ya existe otro rol con ese nombre"
            )
        
        nombre_anterior = rol.name
        permisos_anteriores = sorted(
            self.rol_repository.obtener_ids_permisos_existentes(id_rol)
        )
        
        if permission_ids is not None:
                    permission_ids = validar_permisos(
                        permission_ids,
                        self.rol_repository
                    )
        
        rol_actualizado = self.rol_repository.actualizar_rol(
            id_rol=id_rol,
            nombre=nombre,
            permission_ids=permission_ids
        )
        datos_anteriores: dict = {}
        datos_nuevos: dict = {}
        
        if nombre_cambio:
            datos_anteriores["nombre"] = nombre_anterior
            datos_nuevos["nombre"] = rol_actualizado.name
        
        if permission_ids is not None:
            permisos_nuevos = sorted(set(permission_ids))
            if permisos_nuevos != permisos_anteriores:
                datos_anteriores["permission_ids"] = permisos_anteriores
                datos_nuevos["permission_ids"] = permisos_nuevos
        
        if datos_nuevos:
            self.auditoria.registrar_exito(
                tipo_evento=TipoEvento.USUARIOS,
                accion=AccionEvento.MODIFICAR_ROL,
                entidad=EntidadEvento.ROLES,
                registro_id=str(rol.id),
                datos_nuevos= datos_nuevos,
                datos_anteriores=datos_anteriores,
                contexto=contexto,
            )
        
        return rol_actualizado

class EliminarRol:
    def __init__(self, rol_repository: RolRepositoryPort, auditoria: AuditoriaService):
        self.rol_repository = rol_repository
        self.auditoria = auditoria
    
    def ejecutar(self, id_rol: int, contexto: ContextoAuditoria | None = None):
        rol = self.rol_repository.obtener_por_id(id_rol)
        
        if rol is None:
            raise RolNoEncontrado("El rol solicitado no exite")
        
        if self.rol_repository.tiene_usuarios_asignados(
            id_rol
        ):
            self.auditoria.registrar_fallo(
                tipo_evento=TipoEvento.USUARIOS,
                accion=AccionEvento.ELIMINAR_ROL,
                motivo=MotivoEvento.ROL_CON_USUARIO_ASIGNADO,
                entidad=EntidadEvento.ROLES,
                registro_id=str(id_rol),
                contexto=contexto,
            )
            raise RolConUsuariosAsignados(
                "El rol tiene usuarios asignados"
            )
        
        datos_anteriores = {
            "nombre": rol.name,
            "permission_ids": sorted(self.rol_repository.obtener_ids_permisos_existentes(id_rol)),
        }
        
        self.rol_repository.eliminar_rol(id_rol)
        
        self.auditoria.registrar_exito(
            tipo_evento=TipoEvento.USUARIOS,
            accion=AccionEvento.ELIMINAR_ROL,
            entidad=EntidadEvento.ROLES,
            registro_id=str(id_rol),
            datos_anteriores=datos_anteriores,
            contexto=contexto
        )
