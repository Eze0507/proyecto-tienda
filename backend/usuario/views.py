from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from usuario.serializers import PermisoSerializer, RolSerializer, RolEscrituraSerializer, RolDetalleSerializer
# Create your views here.

class PermisoView(ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermisoSerializer

class RolView(ModelViewSet):
    queryset = Group.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RolSerializer
        if self.action == 'retrieve':
            return RolDetalleSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return RolEscrituraSerializer
        return RolSerializer