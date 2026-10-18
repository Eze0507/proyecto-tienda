from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from backend.seguridad.api.serializers.roles import RolDetalleSerializer, RolListaSerializer
from seguridad.models import Sucursal, Usuario


class SeguridadIntegrationTests(TestCase):
    def test_django_descubre_el_usuario_personalizado_y_ambas_apps(self):
        self.assertIs(get_user_model(), Usuario)
        self.assertIs(apps.get_model("seguridad", "Sucursal"), Sucursal)
        self.assertTrue(apps.is_installed("inventario"))

    def test_rol_serializa_los_usuarios_del_modelo_personalizado(self):
        usuario = Usuario.objects.create_user(
            username="ana",
            password="prueba",
            documento_identidad="12345678",
            departamento_sigla="LP",
        )
        rol = Group.objects.create(name="Administración")
        usuario.groups.add(rol)
        data = RolDetalleSerializer(rol).data
        self.assertEqual(data["usuarios"][0]["id"], usuario.id)
        self.assertEqual(data["permissions"], [])
        self.assertEqual(RolListaSerializer(rol).data["name"], rol.name)

    def test_modelo_aplica_los_validadores_del_dominio(self):
        sucursal = Sucursal(codigo="SUC-A1", nombre="Sucursal 1")
        with self.assertRaises(ValidationError) as error:
            sucursal.full_clean()
        self.assertIn("codigo", error.exception.message_dict)
        self.assertIn("nombre", error.exception.message_dict)

    def test_base_de_datos_impide_dos_sucursales_principales(self):
        Sucursal.objects.create(codigo="SUC-01", nombre="Centro", is_main=True)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Sucursal.objects.create(codigo="SUC-02", nombre="Norte", is_main=True)
