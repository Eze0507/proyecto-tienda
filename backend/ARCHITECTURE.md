# Arquitectura hexagonal del backend

`seguridad` e `inventario` se organizan en cuatro paquetes:

- `domain/`: entidades, objetos de valor, servicios, excepciones y validadores puros de Python. No importa Django, DRF ni adaptadores.
- `application/`: casos de uso y puertos. Depende del dominio; los puertos describen los contratos necesarios para persistencia y servicios externos.
- `infrastructure/`: modelos ORM, repositorios que implementan los puertos y adaptadores de servicios externos.
- `api/`: serializers, vistas, permisos y rutas HTTP. Las vistas delegan las operaciones de negocio a los casos de uso.

La dirección de dependencia es `api → application → domain`. Los adaptadores de infraestructura implementan los contratos de aplicación. Las dependencias concretas se conectan en el borde de entrada cuando se implemente cada caso de uso.

Los archivos con solo una descripción son puntos de extensión; todavía no implementan funcionalidades. Inventario no expone operaciones ni crea tablas hasta definir sus entidades y casos de uso.

## Integración con Django

`apps.py`, `admin.py` y `migrations/` permanecen en la raíz de cada app. Django importa automáticamente `models.py`; por eso `seguridad/models.py` reexporta los modelos de `infrastructure/models.py`. Al agregar modelos de inventario hay que importarlos también desde `inventario/models.py`.

Se usa `AUTH_USER_MODEL = 'seguridad.Usuario'`. Para relaciones nuevas hacia el usuario se debe utilizar `settings.AUTH_USER_MODEL`.

Las rutas de cada módulo se incluyen desde `core/urls.py` bajo `/api/seguridad/` y `/api/inventario/`. Por ahora sus listas de rutas están vacías, pues no había vistas implementadas en seguridad.

## Seguridad existente

Se conservan los campos de `Usuario` y `Sucursal`, sus tablas, permisos y la restricción de sucursal principal única. Se corrigieron las bases de los modelos y la longitud del departamento. `UsuarioSucursal` era un esqueleto vacío: permanece como base abstracta hasta definir sus relaciones y restricciones. `RolUsuarioSerializer` conserva los campos existentes del usuario; se retiró `sucursal` porque ese campo no existe todavía.

Las reglas de formato viven en `domain/validators.py`. `infrastructure/validators.py` convierte `ErrorValidacion` en `django.core.exceptions.ValidationError` para su uso en campos ORM y serializers de DRF. `seguridad/validators.py` mantiene compatibilidad con las rutas anteriores. El validador existente del nombre de sucursal ahora está conectado al campo `nombre`.

Los modelos ORM no ejecutan `full_clean()` automáticamente al llamar `save()`; los casos de uso de escritura y sus adaptadores deberán validar entradas según su contrato, además de las restricciones de la base de datos.

## Verificación y migraciones

Desde `backend/`, con las dependencias instaladas:

```powershell
python manage.py check --settings=core.test_settings
python manage.py test seguridad inventario --settings=core.test_settings
python manage.py makemigrations --check --dry-run --settings=core.test_settings
```

La configuración de pruebas usa SQLite en memoria y no necesita credenciales del entorno. Producción y desarrollo conservan PostgreSQL.

La migración inicial de seguridad se aplica con `python manage.py migrate` en el entorno configurado. No se aplica automáticamente a la base de datos existente. Si ya se migró `auth.User` en esa base, el cambio a un usuario personalizado requiere planificar la migración de datos antes de aplicar este esquema.
