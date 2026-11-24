"""Adaptadores HTTP: autorización y delegación a los casos de uso."""
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from seguridad.infrastructure.repositories.roles import DjangoRolRepository
from seguridad.api.permissions import TienePermiso
from rest_framework.permissions import IsAuthenticated
from seguridad.api.utils.auditoria import obtener_contexto
from seguridad.api.mixins import AuditoriaPermisoMixin
from seguridad.application.services.auditoria import AuditoriaService
from seguridad.infrastructure.repositories.bitacora import DjangoBitacoraRepository

from seguridad.domain.enums import (
    AccionEvento,
    EntidadEvento,
    TipoEvento,
)

from seguridad.api.serializers.roles import (
    RolListaSerializer, 
    RolDetalleSerializer,
    RolCrearSerializer,
    RolActualizarSerializer
)
from seguridad.application.use_cases.roles import (
    ListarRoles, 
    ObtenerDetalleRol, 
    CrearRol,
    ActualizarRol,
    EliminarRol
)

from seguridad.domain.exceptions import (
    RolNoEncontrado,
    RolYaExiste,
    PermisosNoEncontrados,
    RolConUsuariosAsignados
)


class RolListaView(AuditoriaPermisoMixin ,APIView):
    
    permission_classes = [IsAuthenticated, TienePermiso]
    
    permisos_por_metodo = {
        "GET": "auth.view_group",
        "POST": "auth.add_group"
    }
    
    auditoria_tipo_evento = TipoEvento.USUARIOS
    auditoria_entidad = EntidadEvento.ROLES
    auditoria_acciones = {
        "POST": AccionEvento.REGISTRAR_ROL
    }
    
    def get(self, request):
        repository = DjangoRolRepository()
        caso_uso = ListarRoles(repository)

        roles = caso_uso.ejecutar()

        serializer = RolListaSerializer(
            roles,
            many=True
        )

        return Response(serializer.data)
    
    def post(self, request):
        serializer = RolCrearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        datos = serializer.validated_data
        
        repository = DjangoRolRepository()
        auditoria = AuditoriaService(DjangoBitacoraRepository())
        caso_uso = CrearRol(repository, auditoria)
        
        try:
            rol = caso_uso.ejecutar(
                nombre=datos["name"],
                permission_ids=datos["permission_ids"],
                contexto=obtener_contexto(request),
            )
            
        except RolYaExiste as exc:
            raise ValidationError({
                "name": str(exc)
            }) from exc
        
        except PermisosNoEncontrados as exc:
            raise ValidationError({
                "permission_ids": str(exc)
            }) from exc
        
        salida = RolDetalleSerializer(rol)
        
        return Response(
            salida.data,
            status=status.HTTP_201_CREATED
        )

class RolDetalleView(AuditoriaPermisoMixin ,APIView):
    
    permission_classes = [IsAuthenticated, TienePermiso]
    
    permisos_por_metodo = {
        "GET": "auth.view_group",
        "PATCH": "auth.change_group",
        "DELETE": "auth.delete_group"
    }
    
    auditoria_tipo_evento = TipoEvento.USUARIOS
    auditoria_entidad = EntidadEvento.ROLES
    auditoria_pk_kwarg = "pk"
    auditoria_acciones = {
        "PATCH": AccionEvento.MODIFICAR_ROL,
        "DELETE": AccionEvento.ELIMINAR_ROL,
    }
    
    def get(self, request, pk):
        repository = DjangoRolRepository()
        caso_uso = ObtenerDetalleRol(repository)
        
        try:
            rol = caso_uso.ejecutar(id_rol=pk)
        except RolNoEncontrado as exc:
            raise NotFound(str(exc)) from exc
        
        serializer = RolDetalleSerializer(rol)
        
        return Response(serializer.data)
    
    def patch(self, request, pk):
        serializer = RolActualizarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        repository = DjangoRolRepository()
        auditoria = AuditoriaService(DjangoBitacoraRepository())
        caso_uso = ActualizarRol(repository, auditoria)
        
        try:
            rol = caso_uso.ejecutar(
                id_rol=pk,
                nombre=serializer.validated_data.get("name"),
                permission_ids=serializer.validated_data.get("permission_ids"),
                contexto=obtener_contexto(request),
            )
        except RolNoEncontrado as exc:
            raise NotFound(str(exc)) from exc
        
        except RolYaExiste as exc:
            raise ValidationError({
                "name": str(exc)
            }) from exc
        
        except PermisosNoEncontrados as exc:
            raise ValidationError({
                "permission_ids": str(exc)
            }) from exc
        
        salida = RolDetalleSerializer(rol)
        
        return Response(
            salida.data,
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, pk):
        repository = DjangoRolRepository()
        auditoria = AuditoriaService(DjangoBitacoraRepository())
        caso_uso = EliminarRol(repository, auditoria)
        
        try:
            caso_uso.ejecutar(
                id_rol=pk,
                contexto=obtener_contexto(request),
            )
        except RolNoEncontrado as exc:
            raise NotFound(str(exc)) from exc
        except RolConUsuariosAsignados as exc:
            raise ValidationError({
                "rol": str(exc)
            }) from exc
        
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
        
