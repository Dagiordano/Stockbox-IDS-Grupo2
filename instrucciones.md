

Dentro del proyecto, crea una app llamada `inventario`.

### Requisitos:

1. **Modelos en `inventario/models.py`:**
   - `Producto`: nombre, marca, material, estado (choices: nuevo/usado), descripcion.
   - `Prenda`: FK a Producto, talla, color, precio_compra, precio_venta, fecha_creacion, fecha_actualizacion.
   - `Bodega`: ubicacion.
   - `PrendaBodega`: FK a Prenda y a Bodega, campo stock. (unique_together en prenda+bodega).
   - `MovimientoInventario`: FK a PrendaBodega, cantidad, fecha, usuario (FK a User), motivo (choices: ADD, SELL, RETURN).

2. **Vistas en `inventario/views.py`:**
   - Crea funciones para cada CRUD (listar, crear, editar, eliminar) de:
     - Productos
     - Prendas
     - Bodegas
     - PrendaBodega
     - Movimientos
   - Cada vista puede estar vacía, pero debe tener un comentario tipo: 
     ```python
     def lista_productos(request):
         # Aquí va la lógica para listar productos
         pass
     ```

3. **Templates (en `inventario/templates/`):**
   - Crea archivos básicos con solo un `<h1>` que diga qué va en cada página, por ejemplo:
     - `productos_list.html`: `<h1>Aquí va la lista de productos</h1>`
     - `producto_form.html`: `<h1>Aquí va el formulario de producto</h1>`
     - (haz lo mismo para prendas, bodegas, prenda_bodega y movimientos)

4. **URLs:**
   - Configura `inventario/urls.py` con rutas para cada vista de CRUD.
   - Incluye `inventario.urls` en el `urls.py` principal del proyecto.

5. **Autenticación:**
   - Configura login/logout usando los views de Django en `urls.py`.
   - Crea un template `login.html` que diga `<h1>Aquí va el login</h1>`.

6. **Estructura final esperada:**
