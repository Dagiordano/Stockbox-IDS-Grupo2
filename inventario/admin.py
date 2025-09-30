from django.contrib import admin
from .models import Producto, Prenda, Bodega, PrendaBodega, MovimientoInventario

admin.site.register(Producto)
admin.site.register(Prenda)
admin.site.register(Bodega)
admin.site.register(PrendaBodega)
admin.site.register(MovimientoInventario)