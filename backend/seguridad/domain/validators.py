"""Reglas de validación independientes del framework."""

from seguridad.domain.exceptions import ErrorValidacion


def validar_solo_numeros(value: str) -> None:
    if not value.isdigit():
        raise ErrorValidacion("Este campo solo debe contener números.")


def validar_codigo_sucursal(value: str) -> None:
    if not value.startswith("SUC-"):
        raise ErrorValidacion("Debe comenzar con SUC-.")
    numero = value[4:]
    if len(numero) != 2:
        raise ErrorValidacion("Debe tener 2 dígitos después de 'SUC-'.")
    if not numero.isascii() or not numero.isdigit():
        raise ErrorValidacion("Solo se permiten números después de 'SUC-'.")


def validar_solo_letras(value: str) -> None:
    nombre = value.replace(" ", "")
    if not nombre.isalpha():
        raise ErrorValidacion("Este campo solo permite caracteres alfabéticos y espacios.")
