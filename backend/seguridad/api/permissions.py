"""Permisos de acceso de Django REST Framework."""
from rest_framework.permissions import BasePermission

class TienePermiso(BasePermission):
    
    mensaje = "No tienes permiso para realizar esta operacion"
    
    def has_permission(self, request, view):
        
        usuario = request.user
        
        if not usuario.is_authenticated or not usuario.is_active:
            return False
        
        permiso = view.permisos_por_metodo.get(request.method)
        
        if permiso is None:
            return False
        
        return usuario.has_perm(permiso)
