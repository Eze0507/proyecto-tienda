"""Rutas públicas del módulo seguridad."""
from django.urls import path
from seguridad.api.views.roles import RolListaView, RolDetalleView


urlpatterns = [
    path(
        "roles/",
        RolListaView.as_view(),
        name="roles-lista-crear"
    ),
    path(
        "roles/<int:pk>/",
        RolDetalleView.as_view(),
        name="rol-detalle-actualizar-eliminar"
    ),
]