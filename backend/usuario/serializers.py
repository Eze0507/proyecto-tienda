from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User, Group, Permission

#lista de permisos
class PermisoSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'content_type', 'codename']

#lista de roles
class RolSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
#detalle Rol
class RolDetalleSerializer(ModelSerializer):
    permissions = PermisoSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class RolEscrituraSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']