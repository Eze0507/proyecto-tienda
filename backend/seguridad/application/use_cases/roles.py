"""Casos de uso que coordinan el dominio mediante los puertos."""
from seguridad.application.ports.roles import RolRepositoryPort
from seguridad.application.validators import validar_permisos
from seguridad.domain.exceptions import (
    RolNoEncontrado,
    RolYaExiste,
    RolConUsuariosAsignados
)

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
    def __init__(self, rol_repository: RolRepositoryPort):
        self.rol_repository = rol_repository
    
    def ejecutar(
        self,
        nombre: str,
        permission_ids: list[int]
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
        
        return rol

class ActualizarRol:
    def __init__(self, rol_repository: RolRepositoryPort):
        self.rol_repository = rol_repository
    
    def ejecutar(
        self, id_rol: int, 
        nombre: str | None = None, 
        permission_ids: list[int] | None = None
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
        
        if permission_ids is not None:
                    permission_ids = validar_permisos(
                        permission_ids,
                        self.rol_repository
                    )
        
        return self.rol_repository.actualizar_rol(
            id_rol=id_rol,
            nombre=nombre,
            permission_ids=permission_ids
        )

class EliminarRol:
    def __init__(self, rol_repository: RolRepositoryPort):
        self.rol_repository = rol_repository
    
    def ejecutar(self, id_rol: int):
        
        if self.rol_repository.tiene_usuarios_asignados(
            id_rol
        ):
            raise RolConUsuariosAsignados(
                "El rol tiene usuarios asignados"
            )
        
        self.rol_repository.eliminar_rol(id_rol)
