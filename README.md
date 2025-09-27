# StockBox - Sistema de Inventario de Prendas

## Descripción del Proyecto
StockBox es un sistema de gestión de inventario desarrollado en Django para el manejo de prendas de ropa. El proyecto permite administrar productos, prendas, bodegas, stock y movimientos de inventario.

## Estructura del Código

### 1. Configuración Principal (`stockbox/`)
- **`settings.py`**: Configuración principal del proyecto Django
  - Base de datos SQLite configurada
  - App `inventario` incluida en `INSTALLED_APPS`
  - Configuración de templates y middleware estándar
- **`urls.py`**: URLs principales del proyecto
  - Incluye las URLs de la app `inventario`
  - Configuración del panel de administración Django

### 2. Aplicación de Inventario (`inventario/`)

#### Modelos (`models.py`)
El sistema maneja 5 modelos principales:

1. **`Producto`**: Información base de productos
   - Campos: nombre, marca, material, estado (nuevo/usado), descripción
   - Representa la categoría general de un producto

2. **`Prenda`**: Instancia específica de un producto
   - Relación: ForeignKey a Producto
   - Campos: talla, color, precio_compra, precio_venta, fechas
   - Representa una prenda específica con sus características

3. **`Bodega`**: Ubicaciones de almacenamiento
   - Campo: ubicación
   - Representa diferentes lugares donde se almacenan las prendas

4. **`PrendaBodega`**: Relación many-to-many entre Prenda y Bodega
   - Relaciones: ForeignKey a Prenda y Bodega
   - Campo: stock (cantidad disponible)
   - Restricción: unique_together en (prenda, bodega)
   - Controla el inventario de cada prenda en cada bodega

5. **`MovimientoInventario`**: Registro de cambios en el inventario
   - Relación: ForeignKey a PrendaBodega y User
   - Campos: cantidad, fecha, motivo (ADD/SELL/RETURN)
   - Auditoría de todos los movimientos del sistema

#### Vistas (`views.py`)
Implementa operaciones CRUD para cada entidad:
- **Dashboard**: Página principal del sistema
- **Productos**: lista, crear, editar, eliminar
- **Prendas**: lista, crear, editar, eliminar  
- **Bodegas**: lista, crear, editar, eliminar
- **PrendaBodega**: lista, crear, editar, eliminar
- **Movimientos**: lista, crear, editar, eliminar

Todas las vistas están implementadas como funciones básicas que renderizan templates correspondientes.

#### URLs (`urls.py`)
Configuración de rutas para:
- Dashboard principal (`/`)
- Autenticación (`/login/`, `/logout/`)
- CRUD de cada entidad con patrones RESTful:
  - Lista: `/entidad/`
  - Crear: `/entidad/crear/`
  - Editar: `/entidad/editar/<id>/`
  - Eliminar: `/entidad/eliminar/<id>/`

#### Templates (`templates/`)
Estructura de templates para cada funcionalidad:
- `dashboard.html`: Página principal
- `login.html`: Formulario de autenticación
- `productos_list.html`, `producto_form.html`: Gestión de productos
- `prendas_list.html`, `prenda_form.html`: Gestión de prendas
- `bodegas_list.html`, `bodega_form.html`: Gestión de bodegas
- `prenda_bodega_list.html`, `prenda_bodega_form.html`: Gestión de stock
- `movimientos_list.html`, `movimiento_form.html`: Gestión de movimientos

### 3. Base de Datos
- **SQLite** (`db.sqlite3`): Base de datos local para desarrollo
- **Migraciones**: Sistema de migraciones Django para control de versiones de esquema

### 4. Características del Sistema

#### Arquitectura
- **Patrón MVC**: Separación clara entre modelos, vistas y templates
- **CRUD Completo**: Operaciones de creación, lectura, actualización y eliminación
- **Autenticación**: Sistema de login/logout integrado con Django
- **Auditoría**: Registro de movimientos con usuario y fecha

#### Relaciones de Datos
```
Producto (1) → (N) Prenda
Prenda (N) ← → (N) Bodega (a través de PrendaBodega)
PrendaBodega (1) → (N) MovimientoInventario
User (1) → (N) MovimientoInventario
```

#### Flujo de Trabajo
1. Se crean **Productos** (categorías generales)
2. Se crean **Prendas** específicas asociadas a productos
3. Se definen **Bodegas** (ubicaciones de almacenamiento)
4. Se asigna stock de prendas a bodegas (**PrendaBodega**)
5. Se registran **Movimientos** que afectan el stock

### 5. Estado del Proyecto
- ✅ Modelos implementados completamente
- ✅ Vistas CRUD definidas (estructura básica)
- ✅ URLs configuradas
- ✅ Templates creados (estructura básica)
- ✅ Autenticación configurada
- ⏳ Lógica de negocio pendiente de implementación
- ⏳ Interfaz de usuario pendiente de desarrollo

Este proyecto sigue las mejores prácticas de Django y proporciona una base sólida para un sistema de gestión de inventario de prendas.
