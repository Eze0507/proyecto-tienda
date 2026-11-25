from enum import StrEnum

#cerrada pero pendiente de ir agregando mas tipos
class TipoEvento(StrEnum):
    USUARIOS = "USUARIOS"

#cerrada pero pendiente de ir agregando mas acciones
class AccionEvento(StrEnum):
    REGISTRAR_ROL = "REGISTRAR_ROL"
    MODIFICAR_ROL = "MODIFICAR_ROL"
    ELIMINAR_ROL = "ELIMINAR_ROL"

#cerrado
class ResultadoEvento(StrEnum):
    EXITOSO = "EXITOSO"
    FALLIDO = "FALLIDO"

#cerrada pero pendiente de ir agregando mas motivos
class MotivoEvento(StrEnum):
    ROL_CON_USUARIO_ASIGNADO = "ROL_CON_USUARIO_ASIGNADO"
    PERMISO_INSUFICIENTE = "PERMISO_INSUFICIENTE"

#cerrado
class OrigenEvento(StrEnum):
    WEB = "WEB"
    ESCRITORIO = "ESCRITORIO"
    SISTEMA = "SISTEMA"
#cerrada pero pendiente de ir agregando mas entidades
class EntidadEvento(StrEnum):
    ROLES = "ROLES"
