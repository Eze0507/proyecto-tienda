"""Contratos de entrada y salida; no dependen de Django ni de infraestructura."""
from abc import ABC, abstractmethod
from typing import Any
from collections.abc import Iterable

class RolRepositoryPort(ABC):
    
    @abstractmethod
    def Listar(self) -> Iterable[Any]:
        pass
    
    @abstractmethod
    def obtener_detalle(self, id_rol: int) -> Any:
        pass
    
    @abstractmethod
    def existe_por_nombre(self, nombre: str, excluir_rol_id: int | None = None) -> bool:
        pass
    
    @abstractmethod
    def obtener_ids_permisos_existentes(
        self,
        permission_ids: list[int]
    ) -> set[int]:
        pass
    
    @abstractmethod
    def crear_con_permisos(
        self,
        nombre: str,
        permission_ids: list[int]
    ) -> Any:
        pass
    
    @abstractmethod
    def obtener_por_id(
        self, 
        id_rol: int
    ) -> Any:
        pass
    
    @abstractmethod
    def actualizar_rol(
        self,
        id_rol: int, 
        nombre: str | None = None, 
        permission_ids: list[int] | None = None
    ) -> Any:
        pass
    
    @abstractmethod
    def tiene_usuarios_asignados(
        self,
        id_rol
    ) -> bool:
        pass
    
    @abstractmethod
    def eliminar_rol(
        self,
        id_rol
    ) -> None:
        pass

