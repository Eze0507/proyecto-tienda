from rest_framework.request import Request
from seguridad.application.services.auditoria import ContextoAuditoria
from seguridad.domain.enums import OrigenEvento

def obtener_ip(request: Request) -> str | None:
    x_forwarded_for = request.Meta.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.slip(",")[0].strip() or None
    return request.Meta.get("REMOTE_ADDR") or None

#de la capa api obtenemos el id y nombre del usuario, el id y nombre de la sucursal
#la ip del usuario y el origen del usuario en este caso es un endpoint web el origen es web
def obtener_contexto(
    request: Request,
    origen: OrigenEvento = OrigenEvento.WEB,
) -> ContextoAuditoria:
    user = getattr(request, "user", None)
    autenticado = bool(user and user.is_authenticated)
    usuario_id = None
    usuario_nombre = None
    sucursal_id = None
    sucursal_nombre = None
    if autenticado:
        usuario_id = user.id
        usuario_nombre = str(user)
        sucursal = getattr(user, "sucursal", None)
        if sucursal is not None:
            sucursal_id = sucursal.id
            sucursal_nombre = getattr(sucursal, "nombre", None)
    
    return ContextoAuditoria(
        usuario_id=usuario_id,
        usuario_nombre=usuario_nombre,
        sucursal_id=sucursal_id,
        sucursal_nombre=sucursal_nombre,
        ip=obtener_ip(request),
        origen=origen,
    )