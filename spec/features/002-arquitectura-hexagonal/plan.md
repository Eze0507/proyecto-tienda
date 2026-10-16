# 002 · Plan

1. Mover modelos a infrastructure y serializers a api.
2. Extraer validadores a domain y traducir errores en infrastructure.
3. Mantener el descubrimiento de modelos mediante imports en models.py.
4. Registrar ambas apps, configurar AUTH_USER_MODEL y corregir las rutas del proyecto.
5. Generar la migración inicial y verificar con una base de pruebas en memoria.

Los módulos todavía sin casos de uso contienen descripciones de su responsabilidad. UsuarioSucursal permanece abstracto hasta especificar la relación. La configuración normal de PostgreSQL no se modifica y no se aplican migraciones a datos existentes.
