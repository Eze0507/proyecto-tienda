"""Traducción de errores del dominio al contrato de validadores de Django."""

from django.core.exceptions import ValidationError

from seguridad.domain import validators
from seguridad.domain.exceptions import ErrorValidacion


def _validar(validator, value):
    try:
        validator(value)
    except ErrorValidacion as exc:
        raise ValidationError(str(exc), code="invalid") from exc


def validar_solo_numeros(value):
    _validar(validators.validar_solo_numeros, value)


def validar_codigo_sucursal(value):
    _validar(validators.validar_codigo_sucursal, value)


def validar_solo_letras(value):
    _validar(validators.validar_solo_letras, value)
