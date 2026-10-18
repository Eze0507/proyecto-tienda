"""Errores del dominio de seguridad, independientes del framework."""


class ErrorValidacion(ValueError):
    """Un valor incumple las reglas de formato del dominio."""

class RolNoEncontrado(Exception):
    pass

class RolYaExiste(Exception):
    pass

class PermisosNoEncontrados(Exception):
    def __init__(self, ids: list[int]):
        self.ids = ids
        super().__init__(
            f"No existen los permisos con ID: {ids}"
        )

class RolConUsuariosAsignados(Exception):
    pass