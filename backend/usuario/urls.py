from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermisoView, RolView

router = DefaultRouter()

router.register(r'permisos', PermisoView, basename='permiso')
router.register(r'roles', RolView, basename='rol')

urlpatterns = [
    path('', include(router.urls)),
]