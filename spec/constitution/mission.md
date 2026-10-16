# Misión

proporcionando un sistema ERP integral en la nube que centralice el Punto de Venta, el control exacto de inventarios y la seguridad operativa de múltiples sucursales en una sola plataforma en tiempo real

## Qué construimos

Un sistema ERP y Punto de Venta web diseñado a la medida para negocios locales en expansión con hasta 3 sucursales

Elimina el descontrol de inventario y la fuga silenciosa de dinero. Centraliza en tiempo real las ventas, el stock exacto (Kardex) y las ganancias reales, acabando con el caos de cruzar datos a mano entre hojas de Excel, papel y sistemas aislados.

1. **Core de Seguridad (Autenticación y Auditoría)** — Es el guardián del sistema. Gestiona contraseñas encriptadas, roles, permisos y restricciones de horario.
2. **Motor de Inventario (Catálogo y Kardex)** — Es el cerebro físico y valorativo. Centraliza la creación de productos, presentaciones, control de stock por sucursal, alertas de escasez y traspasos.
3. **Abastecimiento (Compras y Proveedores)** — Controla el ingreso de nueva mercadería física y de saldo digital. Maneja órdenes en borrador, compras a crédito y recepciones diferidas (cuando el pago se hace hoy, pero el camión llega mañana).
4. **Punto de Venta Transaccional (POS y Servicios)** — Es la interfaz de alta velocidad para la atención al cliente. Unifica la venta de repuestos físicos con operaciones virtuales (pago de luz, recargas, depósitos/retiros QR) y soporta pagos divididos (ej. mitad efectivo, mitad QR).Su característica clave es la tolerancia a fallos de red: permite seguir registrando ventas locales (offline) que se sincronizan automáticamente con el Kardex central al recuperar la conexión.
5. **Control Operativo (Sesiones y Arqueo de Caja)** — Vigila el comportamiento temporal del dinero físico. Exige un monto de apertura, realiza arqueos ciegos (el cajero cuenta billetes sin saber cuánto debería haber) y bloquea operaciones si el turno expira.
6. **Backoffice Financiero y Analítica (El Panel del Dueño)** — Es el libro contable inmutable. Registra todos los ingresos y egresos separando el dinero de caja del dinero del administrador. Calcula gastos operativos fijos/variables y genera el cierre mensual.

## Para quién

- **Usuario o público principal y qué busca**: Dueños y administradores de negocios locales en expansión (hasta 3 sucursales, como talleres mecánicos o minimarkets). Buscan centralizar el control de su inventario, conocer su ganancia neta real (mediante Kardex inmutable y costo promedio ponderado) y auditar toda su operación para evitar fugas de dinero o fraudes, accediendo a esta información desde un panel de control remoto y en tiempo real.
- **Usuario secundario**: Cajeros y personal operativo en mostrador. Necesitan una interfaz de Punto de Venta (POS) aislada, rápida y a prueba de errores. Buscan agilidad para cobrar repuestos, procesar recargas y servicios, operando bajo un entorno seguro de sesiones de caja y arqueos ciegos que delimite y proteja su responsabilidad sobre el dinero físico.

## Principios

_Las ideas rectoras que guían las decisiones de producto y técnicas. 3-5 puntos._

- **Inmutabilidad de la Historia Financiera** — Implica que los datos transaccionales, de inventario (Kardex) y monetarios nunca se eliminan físicamente de la base de datos (DELETE). En la práctica, se utilizan bajas lógicas (Soft Delete con esta_activo=False), anulación de documentos con contra-asientos compensatorios y bloqueos (on_delete=PROTECT) para garantizar que la auditoría sea 100% confiable y rastreable.
- **Revelación Progresiva y Contextos Aislados** — Implica que la interfaz gráfica no debe abrumar al usuario y se adapta a su rol. En la práctica, significa separar el frontend usando Lazy Loading (un Punto de Venta ágil y libre de distracciones vs. un Backoffice analítico) y utilizar el patrón "Micro/Macro" (pestañas dentro del producto para el detalle, tablas globales para la auditoría general).
- **Exactitud Contable Automatizada** — Implica que el sistema asume la carga matemática para evitar el error humano y la fuga de capital. En la práctica, el backend recalcula obligatoriamente el Costo Promedio Ponderado tras cada compra recibida, y separa de forma estricta el dinero de la Sesión de Caja (mostrador) del flujo de capital del Administrador (billeteras/backoffice) para garantizar un arqueo ciego perfecto.
- **Fricción Cero en la Captura de Datos Maestros** — Implica optimizar la experiencia de usuario (UX) asumiendo el alcance acotado del sistema (máximo 3 sucursales). En la práctica, se utilizan "Formularios Compuestos" para crear el Producto, la Presentación y el Stock Inicial en un solo paso, utilizando la Inicialización Anticipada (Eager Initialization) para generar automáticamente las filas de stock en cero en la base de datos sin obligar al usuario a hacer configuraciones repetitivas.


## Qué NO es

- **No es un ERP de escala corporativa o franquicias masivas**: El sistema está diseñado y optimizado arquitectónicamente para un máximo de 3 sucursales físicas operando bajo una misma razón social. Deliberadamente no incluye gestión de almacenes intermedios (centros de distribución de tránsito), ni soporte para logística compleja de importaciones o aduanas.
- **No es un software contable legal ni tributario**: Aunque el sistema calcula con exactitud el Costo Promedio Ponderado, la ganancia neta y audita las finanzas internas, no pretende reemplazar al contador. No emite balances generales, libros mayores, cálculos de depreciación de activos, ni realiza integraciones directas con sistemas de impuestos nacionales para declaraciones juradas (emite notas de venta o recibos de consumo interno).
- **No incluye módulos de Recursos Humanos ni planillas**: Si bien el sistema gestiona cuentas de usuario, vigila el horario de inicio de sesión y registra el rendimiento por cajero, no está diseñado para calcular sueldos, horas extras, vacaciones, ni gestionar los beneficios sociales del personal.
- **No es una plataforma de E-commerce orientada al consumidor**: El proyecto es una herramienta de uso estrictamente interno (Backoffice y POS). No incluye catálogos en línea para que los clientes finales hagan compras desde sus casas, ni aplicaciones móviles de fidelización de clientes. Toda la operación ocurre presencialmente en el mostrador o por gestión telefónica registrada por un empleado.