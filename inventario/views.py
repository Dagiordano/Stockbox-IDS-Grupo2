from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto, Prenda, Bodega, PrendaBodega, MovimientoInventario


# Create your views here.



def home(request):
    return render(request, 'home.html')

# Dashboard
def dashboard(request):
    # logica para el dashboard
    return render(request, 'dashboard.html')



# Productos CRUD
def lista_productos(request):
    # logica para listar productos
   
    return render(request, 'productos_list.html')

def crear_producto(request):
    # logica para crear producto
    return render(request, 'producto_form.html')

def editar_producto(request, id):
    # logica para editar producto
    return render(request, 'producto_form.html')

def eliminar_producto(request, id):
    # logica para eliminar producto
    return render(request, 'productos_list.html')



# Prendas CRUD
def lista_prendas(request):
    # logica para listar prendas
    return render(request, 'prendas_list.html')

def crear_prenda(request):
    # logica para crear prenda
    return render(request, 'prenda_form.html')

def editar_prenda(request, id):
    # logica para editar prenda
    return render(request, 'prenda_form.html')

def eliminar_prenda(request, id):
    # logica para eliminar prenda
    return render(request, 'prendas_list.html')



# Bodegas CRUD
def lista_bodegas(request):
    # logica para listar bodegas
    return render(request, 'bodegas_list.html')

def crear_bodega(request):
    # logica para crear bodega
    return render(request, 'bodega_form.html')

def editar_bodega(request, id):
    # logica para editar bodega
    return render(request, 'bodega_form.html')

def eliminar_bodega(request, id):
    # logica para eliminar bodega
    return render(request, 'bodegas_list.html')



# PrendaBodega CRUD
def lista_prenda_bodega(request):
    # logica para listar prenda bodega
    return render(request, 'prenda_bodega_list.html')

def crear_prenda_bodega(request):
    # logica para crear prenda bodega
    return render(request, 'prenda_bodega_form.html')

def editar_prenda_bodega(request, id):
    # logica para editar prenda bodega
    return render(request, 'prenda_bodega_form.html')

def eliminar_prenda_bodega(request, id):
    # logica para eliminar prenda bodega
    return render(request, 'prenda_bodega_list.html')



# Movimientos CRUD
def lista_movimientos(request):
    # logica para listar movimientos
    return render(request, 'movimientos_list.html')

def crear_movimiento(request):
    # logica para crear movimiento
    return render(request, 'movimiento_form.html')

def editar_movimiento(request, id):
    # logica para editar movimiento
    return render(request, 'movimiento_form.html')

def eliminar_movimiento(request, id):
    # logica para eliminar movimiento
    return render(request, 'movimientos_list.html')
