# 002 · Arquitectura hexagonal

**Estado:** implementado

## Qué hace

Reorganiza seguridad y crea la base de inventario con los paquetes domain, application, infrastructure y api.

## Criterios de aceptación

- [x] Ambas apps contienen los archivos de las cuatro capas solicitadas.
- [x] Se conservan los modelos y serializers existentes, corrigiendo los errores que impedían utilizarlos.
- [x] Las reglas de validación no dependen de Django; sus adaptadores mantienen el contrato del ORM.
- [x] Django descubre el usuario personalizado y ambas aplicaciones.
- [x] Inventario queda preparado sin agregar funcionalidades de negocio no especificadas.

## Fuera de alcance

CRUD, autenticación HTTP, entidades de inventario y definición de la relación UsuarioSucursal.
