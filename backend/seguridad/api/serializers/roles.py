from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from seguridad.models import Usuario

class RolUsuarioSerializer(serializers.ModelSerializer):
    sucursales = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="nombre"
    )
    class Meta:
        model = Usuario
        fields = [
            "id", 
            "first_name", 
            "last_name", 
            "is_active",
            "sucursales"
            ]

class PermisoSerializer(serializers.ModelSerializer):
    #id del modelo al que pertenece un permiso
    modelo_id = serializers.IntegerField(
        source="content_type_id",
        read_only=True
    )
    #nombre del modelo al que pertenece un permiso
    modelo = serializers.CharField(
        source="content_type.model",
        read_only=True
    )
    #nombre de la app a la que pertenece un permiso
    app = serializers.CharField(
        source="content_type.app_label"
    )
    class Meta:
        model = Permission
        fields = [
            "id", 
            "name", 
            "codename",
            "modelo_id",
            "modelo",
            "app"
            ]

class RolListaSerializer(serializers.ModelSerializer):
    cantidad_usuarios_activos = serializers.IntegerField(
        read_only=True
    )
    class Meta:
        model = Group
        fields = [
            "id", 
            "name",
            "cantidad_usuarios_activos"
            ]

class RolDetalleSerializer(serializers.ModelSerializer):
    permissions = PermisoSerializer(
        many=True, 
        read_only=True
        )
    usuarios = RolUsuarioSerializer(
        source="user_set",
        many=True,
        read_only=True
        )
    class Meta:
        model = Group
        fields = [
            "id", 
            "name", 
            "permissions", 
            "usuarios"
            ]

class RolCrearSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list
    )

class RolActualizarSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=150,
        required=False
    )
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )