from unittest import TestCase

from django.core.exceptions import ValidationError

from seguridad.domain.exceptions import ErrorValidacion
from seguridad.domain.validators import (
    validar_codigo_sucursal,
    validar_nombre_sucursal,
    validar_solo_numeros,
)
from seguridad.infrastructure import validators as django_validators


class ValidadoresTests(TestCase):
    def test_documentos_y_telefonos_numericos(self):
        validar_solo_numeros("00123456")
        for value in ("", "123a", "12 34", "-123"):
            with self.subTest(value=value), self.assertRaises(ErrorValidacion):
                validar_solo_numeros(value)

    def test_codigo_sucursal_exige_prefijo_y_dos_digitos(self):
        validar_codigo_sucursal("SUC-01")
        for value in ("", "suc-01", "SUC-1", "SUC-001", "SUC-AA", "SUC-²²"):
            with self.subTest(value=value), self.assertRaises(ErrorValidacion):
                validar_codigo_sucursal(value)

    def test_nombre_permite_letras_acentos_y_espacios(self):
        validar_nombre_sucursal("Sucursal Peña")
        for value in ("", "   ", "Sucursal 1", "Sucursal!"):
            with self.subTest(value=value), self.assertRaises(ErrorValidacion):
                validar_nombre_sucursal(value)

    def test_adaptadores_traducen_errores_para_django(self):
        for validator, value in (
            (django_validators.validar_solo_numeros, "abc"),
            (django_validators.validar_codigo_sucursal, "SUC-X"),
            (django_validators.validar_nombre_sucursal, "123"),
        ):
            with self.subTest(validator=validator), self.assertRaises(ValidationError):
                validator(value)
