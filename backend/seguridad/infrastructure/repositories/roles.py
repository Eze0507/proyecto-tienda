"""Adaptadores de persistencia que implementan los puertos de aplicación."""
from django.contrib.auth.models import Group, Permission
from backend.seguridad.application.ports.roles import RolRepositoryPort
from django.db.models import Count, Q, Prefetch, QuerySet
from seguridad.models import Usuario
from django.db import transaction, IntegrityError
from seguridad.domain.exceptions import RolYaExiste, RolNoEncontrado

class DjangoRolRepository(RolRepositoryPort):
    
    def Listar(self) -> QuerySet[Group]:
                return (
            Group.objects.annotate(
                cantidad_usuarios_activos=Count(
                    "user", filter=Q(user_is_active=True)
                )
            ).order_by("name")
        )
    
    def obtener_detalle(self, id_rol: int) -> Group | None:
            return (
                Group.objects.prefetch_related(
                    "permissions_content_type",
                    Prefetch(
                        "user_set",
                        queryset=Usuario.objects.prefetch_related("sucursale")
                    )
                )
                .filter(id=id_rol)
                .first()
            )
    
    def existe_por_nombre(self, nombre: str, excluir_rol_id: int | None = None) -> bool:
            consulta = Group.objects.filter(name=nombre)
            
            if excluir_rol_id is not None:
                consulta = consulta.exclude(id=excluir_rol_id)
            
            return consulta.exists()
    
    def obtener_ids_permisos_existentes(self, permission_ids: list[int]) -> set[int]:
            return set(
                Permission.objects.filter(
                    id_in=permission_ids
                ).values_list("id", flat=True)
            )
    
    def crear_con_permisos(self, nombre: str, permission_ids: list[int]) -> Group:
            try:
                with transaction.atomic():
                    
                    rol = Group.objects.create(
                        name=nombre
                    )
                    
                    rol.permissions.set(permission_ids)
                    
                    return rol
            except IntegrityError as exc:
                raise RolYaExiste(
                    "ya existe un rol con ese nombre"
                ) from exc
    
    def obtener_por_id(self, id_rol: int) -> Group | None:
            try:
                rol = Group.objects.get(id=id_rol)
            except Group.DoesNotExist as exc:
                raise RolNoEncontrado(
                    "El rol solicitado no existe"
                ) from exc
            
            return rol
    
    def actualizar_rol(self, id_rol, nombre: str | None = None, permission_ids: list[int] | None = None) -> Group:  
            with transaction.atomic():
                try:
                    rol = Group.objects.get(id=id_rol)
                except Group.DoesNotExist as exc:
                    raise RolNoEncontrado(
                        "El rol solicitado para la actualizacion no existe"
                    ) from exc
                
                if nombre is not None and nombre != rol.name :
                    rol.name = nombre
                    rol.save(update_fields=["name"])
                    
                if permission_ids is not None:
                    rol.permissions.set(permission_ids)
                
                return rol
    
    def tiene_usuarios_asignados(self, id_rol):
            return Usuario.objects.filter(
                Groups_id=id_rol
            ).exists
    
    def eliminar_rol(self, id_rol):
            try:
                rol = Group.objects.get(id=id_rol)
            except Group.DoesNotExist as exc:
                raise RolNoEncontrado(
                    "El rol solicitado para la eliminacion no existe"
                ) from exc
            
            rol.delete()
