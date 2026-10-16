# Tech stack y convenciones

Cómo está construido el proyecto y las reglas técnicas globales que todo el código debe respetar. Es la referencia que ningún `plan.md` de una feature debe contradecir.

Este documento describe la arquitectura objetivo del ERP/POS. Las rutas indican la organización prevista y no implican que todos los módulos estén implementados. Una decisión marcada como **PENDIENTE** debe resolverse y documentarse antes de desarrollar una funcionalidad que dependa de ella.

---

## Tecnologías

- **Backend:** Python 3.14 + Django + Django REST Framework.
- **Frontend administrativo:** TypeScript estricto + Angular + HTML + CSS.
- **POS de escritorio:** Angular + Tauri 2.
- **Base de datos central:** PostgreSQL, accedida desde Django mediante su ORM.
- **Base de datos local del POS:** SQLite.
- **Contenedores:** Docker + Docker Compose para backend, PostgreSQL y servicios auxiliares del entorno.
- **Servidor backend:** Gunicorn.
- **Servidor del Backoffice Web:** Nginx sirviendo la aplicación Angular compilada.
- **Despliegue en la nube:** **PENDIENTE**.

PostgreSQL es la fuente de verdad central del sistema. SQLite existe únicamente como almacenamiento operativo local del POS para permitir funcionamiento sin conexión y sincronización posterior.

Redis, Service Worker, Cache Storage, IndexedDB y Dexie **no forman parte del stack base actual**. Solo podrán incorporarse si una necesidad futura concreta lo justifica y queda documentada.

---

## Archivos / módulos clave

_Mapa breve de las responsabilidades principales del backend._

- `backend/seguridad/` — autenticación, usuarios, roles, permisos, restricciones de acceso y auditoría de seguridad.
- `backend/inventario/` — productos, presentaciones, stock por sucursal, Kardex, movimientos de inventario y Costo Promedio Ponderado.
- `backend/compras/` — compras de productos, compras al contado o crédito, pagos, recepción diferida de mercadería y abastecimiento de saldo digital.
- `backend/pos/` — ventas de productos, recargas, servicios, depósitos/retiros y pagos realizados desde el Punto de Venta.
- `backend/caja/` — sesiones de caja, apertura, movimientos de efectivo, cierre y arqueo ciego.
- `backend/finanzas/` — movimientos financieros, billeteras, ingresos, egresos, gastos y consolidación financiera del negocio.

Cada aplicación es propietaria de sus datos y de las reglas de negocio asociadas a ellos.

---

## Comandos

- `docker compose up --build` — construye y arranca el entorno local.

Otros comandos se documentarán cuando su uso sea estable dentro del proyecto.

---

## Arquitectura

- **Arquitectura del sistema:** Cliente-Servidor + Monolito Modular.
- **Arquitectura de datos:** PostgreSQL relacional, single-tenant y multi-sucursal.
- **Inventario:** cada sucursal mantiene stock independiente; no existe un stock físico central compartido entre sucursales.
- **Backend:** API REST organizada por módulos de dominio con arquitectura hexagonal (`domain`, `application`, `infrastructure`, `api`).
- **Frontend:** dos aplicaciones cliente consumen la misma API:
  - **Backoffice Web:** Angular, funcionamiento online.
  - **POS Desktop:** Angular + Tauri 2, con funcionamiento offline y sincronización posterior.
- **Fuente de verdad:** Django + PostgreSQL tienen autoridad sobre los datos definitivos del sistema.

Las sucursales pertenecen a la misma empresa y comparten el mismo sistema. Una sucursal no constituye un tenant independiente.

---

## Convenciones

### 1. Nomenclatura

**Backend — Django**

- `PascalCase` para clases y modelos: `DetalleVenta`.
- `snake_case` para funciones, variables, módulos y archivos: `descontar_stock()`.
- `UPPER_SNAKE_CASE` para constantes: `ESTADO_ACTIVO`.

**Frontend — Angular**

- `PascalCase` para clases, componentes e interfaces: `ProductListComponent`.
- `camelCase` para variables, propiedades y métodos: `calculateTotal()`.
- `kebab-case` para nombres de archivos: `product-list.component.ts`.

### 2. Organización de pruebas

**Django**

Eliminar el `tests.py` genérico y utilizar una carpeta `tests/` por aplicación.

```text
inventario/
└── tests/
    ├── test_models.py
    ├── test_services.py
    └── test_api.py
```

**Angular**

Los tests unitarios permanecen junto al archivo probado:

```text
pos.component.ts
pos.component.spec.ts
```

### 3. Responsabilidades por capa

Cada aplicación del backend utiliza arquitectura hexagonal:

- **`domain/entities.py` y `value_objects.py`:** entidades y objetos de valor independientes del framework.
- **`domain/services.py`, `validators.py` y `exceptions.py`:** reglas de negocio, validaciones y errores de dominio sin dependencias de Django o DRF.
- **`application/use_cases.py`:** coordinación de operaciones mediante el dominio y los puertos.
- **`application/ports.py`:** contratos de persistencia y servicios requeridos por los casos de uso.
- **`infrastructure/models.py`:** modelos Django, relaciones y restricciones de base de datos.
- **`infrastructure/repositories.py` y `external_services.py`:** adaptadores que implementan los puertos.
- **`api/serializers.py`:** representación y validación estructural de entrada/salida.
- **`api/views.py`, `permissions.py` y `urls.py`:** HTTP, autorización y delegación a casos de uso.

El dominio no importa las otras capas ni frameworks. Aplicación depende del dominio y declara los puertos; infraestructura implementa esos contratos. Los adaptadores de entrada conectan las implementaciones concretas. La lógica de negocio no debe implementarse en Views ni Serializers.

`models.py` en la raíz de cada app reexporta los modelos ORM para que Django los descubra. `apps.py`, `admin.py` y `migrations/` permanecen en la raíz. Ver `backend/ARCHITECTURE.md` para detalles de integración.

### 4. Errores y validación

- Angular valida anticipadamente los formularios para mejorar la experiencia del usuario.
- Los Serializers validan estructura, formato y restricciones de entrada.
- El dominio valida las reglas de negocio y los casos de uso coordinan su ejecución.
- Las reglas críticas siempre deben volver a validarse en el backend.
- No confiar en validaciones realizadas únicamente por el frontend o por el POS offline.
- Para errores de dominio reutilizables, preferir excepciones específicas en lugar de depender únicamente de `ValueError`.
- La API debe devolver códigos HTTP coherentes y errores con una estructura consistente.
- Angular puede centralizar el manejo de errores HTTP mediante interceptores.

Ejemplos de excepciones de dominio:

```python
StockInsuficienteError
SesionCajaCerradaError
OperacionNoPermitidaError
```

### 5. Idioma del código

**Español**

Utilizar para conceptos propios del dominio:

```text
Venta
Compra
Producto
calcular_costo_promedio()
```

**Inglés**

Mantener nombres establecidos por Django, Angular, Tauri, bibliotecas y protocolos:

```text
is_active
request
response
GET
POST
```

No traducir nombres propios del framework.

---

## Persistencia e integridad

### Atomicidad

Toda operación de negocio que modifique varios registros dependientes debe ejecutarse dentro de una transacción:

```python
with transaction.atomic():
    ...
```

Ejemplos:

- confirmar una venta;
- recibir una compra;
- registrar movimientos relacionados de inventario;
- registrar movimientos financieros asociados;
- confirmar una transferencia entre sucursales.

Una operación debe completarse completamente o revertirse completamente.

### Propiedad de los datos

Cada módulo es responsable de modificar sus propias entidades.

Una aplicación no debe modificar directamente datos pertenecientes a otra aplicación cuando exista un servicio público encargado de realizar esa operación.

Ejemplo conceptual:

```text
pos
 └── solicita a inventario
      └── registrar_salida(...)
```

en lugar de modificar directamente el stock desde `pos`.

Las consultas entre módulos están permitidas cuando sean necesarias. Cuando una consulta contenga lógica reutilizable o de dominio, debe exponerse mediante una interfaz pública del módulo propietario, mediante un puerto o caso de uso público del módulo.

### Relaciones entre aplicaciones

Para relaciones Django hacia modelos de otra aplicación utilizar referencias lazy por nombre:

```python
models.ForeignKey(
    "inventario.Producto",
    on_delete=models.PROTECT,
)
```

Esto evita imports innecesarios, aunque la relación sigue representando una dependencia estructural entre ambos módulos.

No crear dependencias circulares entre módulos.

---

## Inmutabilidad y borrado

Los datos históricos o transaccionales confirmados no deben eliminarse físicamente.

Distinguir tres casos:

- **Datos maestros:** se desactivan cuando corresponda, por ejemplo con `esta_activo = False`.
- **Documentos transaccionales:** se anulan mediante estados y, cuando corresponda, movimientos compensatorios.
- **Movimientos históricos:** no se modifican ni eliminan para ocultar o reemplazar operaciones pasadas.

Ejemplos de información histórica:

```text
Venta
Compra
MovimientoInventario
MovimientoFinanciero
DetalleVenta confirmado
DetalleCompra confirmado
```

Utilizar `on_delete=PROTECT` cuando eliminar una entidad pueda destruir la trazabilidad histórica.

---

## Offline

El modo offline existe exclusivamente en el **POS Desktop**. El Backoffice Web requiere conexión con el backend.

### Persistencia local

- El POS utiliza **SQLite** como base de datos local.
- SQLite contiene únicamente los datos necesarios para operar el Punto de Venta y las operaciones todavía no sincronizadas.
- La base local no reemplaza a PostgreSQL ni constituye una segunda fuente de verdad.
- Los datos sincronizados podrán mantenerse localmente como caché operativa cuando sean necesarios para seguir trabajando sin conexión.

### Identidad

Las entidades que puedan originarse en el POS sin conexión deben utilizar identificadores UUID generados antes de comunicarse con el backend.

No todas las entidades del sistema necesitan UUID; la elección depende de si su identidad debe existir antes de llegar al servidor o de otras necesidades del dominio.

### Sincronización

El POS debe:

- registrar operaciones localmente cuando no exista conexión;
- mantener una cola de operaciones pendientes de sincronización;
- sincronizar automáticamente al recuperar conexión;
- utilizar idempotencia para que reenviar una operación no genere duplicados;
- enviar operaciones compuestas de forma completa;
- reconciliar los datos locales con la respuesta autoritativa del backend.

Cuando sea conveniente, el Sync Engine puede agrupar operaciones pendientes mediante batching.

La estrategia detallada de sincronización y resolución de conflictos debe definirse en el `plan.md` de las features que dependan de ella.

### Autoridad

El POS puede mantener proyecciones locales necesarias para continuar operando, pero Django es responsable de confirmar definitivamente:

- ventas;
- movimientos de inventario;
- Kardex;
- Costo Promedio Ponderado;
- movimientos financieros;
- estados definitivos de caja;
- permisos y reglas de negocio.

El backend debe volver a validar toda operación recibida desde un POS que trabajó offline.

---

## Límites duros

### Dependencias

1. No modificar directamente datos pertenecientes a otro módulo cuando exista un servicio público para realizar la operación.
2. No crear dependencias circulares entre módulos.
3. No utilizar imports cruzados innecesarios de modelos para ejecutar reglas de negocio de otra aplicación.
4. Las relaciones Django entre aplicaciones deben utilizar referencias lazy por nombre cuando sea posible.

### Lógica de negocio

1. No colocar reglas de negocio, cálculos financieros ni cálculos de inventario en `views.py` o `serializers.py`.
2. No colocar modelos ni lógica de negocio dentro del paquete de configuración principal (`core/`, `config/` o equivalente).
3. No duplicar una regla crítica como dos implementaciones autoritativas distintas en frontend y backend.
4. La validación definitiva siempre pertenece al backend.

### Integridad

1. Nunca realizar escrituras dependientes sin atomicidad.
2. Nunca permitir que el frontend determine directamente el Kardex, el Costo Promedio Ponderado o los movimientos financieros definitivos.
3. Nunca eliminar físicamente información transaccional confirmada para corregir un error.
4. Nunca confiar en datos provenientes del POS offline sin volver a validar permisos, sucursal, estado de caja, consistencia e invariantes de negocio en el backend.
5. Toda operación que afecte stock debe ejecutarse dentro del contexto de una sucursal concreta; nunca asumir stock global.

---

## Decisiones pendientes

Las siguientes decisiones todavía no forman parte obligatoria de la arquitectura:

- proveedor de despliegue en la nube;
- librería o plugin concreto para acceder a SQLite desde Tauri 2;
- almacenamiento seguro de credenciales/tokens del POS;
- formato exacto de la cola de sincronización;
- estrategia completa de reintentos y resolución de conflictos del Sync Engine.

Una feature que dependa de una decisión pendiente debe resolverla primero en su `plan.md` o promoverla a este documento si pasa a convertirse en una regla global del proyecto.