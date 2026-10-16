from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from seguridad.infrastructure.models import Usuario

class RolUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "first_name", "last_name", "is_active"]

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "content_type_id"]

class RolListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

class RolDetalleSerializer(serializers.ModelSerializer):
    permissions = PermisoSerializer(many=True, read_only=True)
    usuarios = RolUsuarioSerializer(source="user_set", many=True, read_only=True)
    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "usuarios"]