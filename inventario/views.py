from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Dashboard
def dashboard(request):
    # Aquí va la lógica para el dashboard
    return render(request, 'dashboard.html')

# Productos CRUD
def lista_productos(request):
    # Aquí va la lógica para listar productos
    return render(request, 'productos_list.html')

def crear_producto(request):
    # Aquí va la lógica para crear producto
    return render(request, 'producto_form.html')

def editar_producto(request, id):
    # Aquí va la lógica para editar producto
    return render(request, 'producto_form.html')

def eliminar_producto(request, id):
    # Aquí va la lógica para eliminar producto
    return render(request, 'productos_list.html')

# Prendas CRUD
def lista_prendas(request):
    # Aquí va la lógica para listar prendas
    return render(request, 'prendas_list.html')

def crear_prenda(request):
    # Aquí va la lógica para crear prenda
    return render(request, 'prenda_form.html')

def editar_prenda(request, id):
    # Aquí va la lógica para editar prenda
    return render(request, 'prenda_form.html')

def eliminar_prenda(request, id):
    # Aquí va la lógica para eliminar prenda
    return render(request, 'prendas_list.html')

# Bodegas CRUD
def lista_bodegas(request):
    # Aquí va la lógica para listar bodegas
    return render(request, 'bodegas_list.html')

def crear_bodega(request):
    # Aquí va la lógica para crear bodega
    return render(request, 'bodega_form.html')

def editar_bodega(request, id):
    # Aquí va la lógica para editar bodega
    return render(request, 'bodega_form.html')

def eliminar_bodega(request, id):
    # Aquí va la lógica para eliminar bodega
    return render(request, 'bodegas_list.html')

# PrendaBodega CRUD
def lista_prenda_bodega(request):
    # Aquí va la lógica para listar prenda bodega
    return render(request, 'prenda_bodega_list.html')

def crear_prenda_bodega(request):
    # Aquí va la lógica para crear prenda bodega
    return render(request, 'prenda_bodega_form.html')

def editar_prenda_bodega(request, id):
    # Aquí va la lógica para editar prenda bodega
    return render(request, 'prenda_bodega_form.html')

def eliminar_prenda_bodega(request, id):
    # Aquí va la lógica para eliminar prenda bodega
    return render(request, 'prenda_bodega_list.html')

# Movimientos CRUD
def lista_movimientos(request):
    # Aquí va la lógica para listar movimientos
    return render(request, 'movimientos_list.html')

def crear_movimiento(request):
    # Aquí va la lógica para crear movimiento
    return render(request, 'movimiento_form.html')

def editar_movimiento(request, id):
    # Aquí va la lógica para editar movimiento
    return render(request, 'movimiento_form.html')

def eliminar_movimiento(request, id):
    # Aquí va la lógica para eliminar movimiento
    return render(request, 'movimientos_list.html')
