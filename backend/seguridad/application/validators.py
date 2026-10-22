from seguridad.application.ports.roles import RolRepositoryPort
from seguridad.domain.exceptions import (
    RolNoEncontrado,
    RolYaExiste,
    PermisosNoEncontrados
)

def validar_permisos(
    permission_ids: list[int], 
    repositorio: RolRepositoryPort
) -> list[int]:
    
    ids_unicos = list(dict.fromkeys(permission_ids))
    
    ids_existentes = (
        repositorio.obtener_ids_permisos_existentes(
            ids_unicos
        )
    )
    
    ids_faltantes = set(ids_unicos) - ids_existentes
    
    if ids_faltantes:
        raise PermisosNoEncontrados(
            sorted(ids_faltantes)
        )
    
    return ids_unicos