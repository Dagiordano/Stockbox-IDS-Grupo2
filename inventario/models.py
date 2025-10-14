from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
    ]
    
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('unisex', 'Unisex'),
    ]
    
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=50, default="General")
    marca = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='nuevo')
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, default='unisex')
    descripcion = models.TextField(blank=True)

    proveedor = models.CharField(max_length=100, blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.PositiveIntegerField(default=0)
    
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.sku}"

class Prenda(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=10)
    color = models.CharField(max_length=30)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.talla} - {self.color}"

class Bodega(models.Model):
    ubicacion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.ubicacion

class PrendaBodega(models.Model):
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('prenda', 'bodega')
    
    def __str__(self):
        return f"{self.prenda} en {self.bodega} - Stock: {self.stock}"

class MovimientoInventario(models.Model):
    MOTIVO_CHOICES = [
        ('ADD', 'Agregar'),
        ('SELL', 'Vender'),
        ('RETURN', 'Devolver'),
    ]
    
    prenda_bodega = models.ForeignKey(PrendaBodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    motivo = models.CharField(max_length=10, choices=MOTIVO_CHOICES)
    
    def __str__(self):
        return f"{self.prenda_bodega} - {self.cantidad} - {self.motivo}"
