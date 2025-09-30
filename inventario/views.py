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
    productos = Producto.objects.all()
    return render(request, 'productos_list.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        material = request.POST.get('material')
        estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion', '')
        
        Producto.objects.create(
            nombre=nombre,
            marca=marca,
            material=material,
            estado=estado,
            descripcion=descripcion
        )
        
        messages.success(request, 'Producto creado exitosamente')
        return redirect('lista_productos')
    

    estados = Producto.ESTADO_CHOICES
    return render(request, 'producto_form.html', {'estados': estados})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.marca = request.POST.get('marca')
        producto.material = request.POST.get('material')
        producto.estado = request.POST.get('estado')
        producto.descripcion = request.POST.get('descripcion', '')
        producto.save()
        
        messages.success(request, 'Producto actualizado exitosamente')
        return redirect('lista_productos')
    
    estados = Producto.ESTADO_CHOICES
    return render(request, 'producto_form.html', {'producto': producto, 'estados': estados})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
    
    return redirect('lista_productos')



# Prendas CRUD
def lista_prendas(request):
    prendas = Prenda.objects.all().select_related('producto')
    return render(request, 'prendas_list.html', {'prendas': prendas})

def crear_prenda(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        talla = request.POST.get('talla')
        color = request.POST.get('color')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        
        Prenda.objects.create(
            producto_id=producto_id,
            talla=talla,
            color=color,
            precio_compra=precio_compra,
            precio_venta=precio_venta
        )
        
        messages.success(request, 'Prenda creada exitosamente')
        return redirect('lista_prendas')
    
    productos = Producto.objects.all()
    return render(request, 'prenda_form.html', {'productos': productos})

def editar_prenda(request, id):
    prenda = get_object_or_404(Prenda, id=id)
    
    if request.method == 'POST':
        prenda.producto_id = request.POST.get('producto')
        prenda.talla = request.POST.get('talla')
        prenda.color = request.POST.get('color')
        prenda.precio_compra = request.POST.get('precio_compra')
        prenda.precio_venta = request.POST.get('precio_venta')
        prenda.save()
        
        messages.success(request, 'Prenda actualizada exitosamente')
        return redirect('lista_prendas')
    
    productos = Producto.objects.all()
    return render(request, 'prenda_form.html', {'prenda': prenda, 'productos': productos})

def eliminar_prenda(request, id):
    prenda = get_object_or_404(Prenda, id=id)
    
    if request.method == 'POST':
        prenda.delete()
        messages.success(request, 'Prenda eliminada exitosamente')
    
    return redirect('lista_prendas')




# Bodegas CRUD
def lista_bodegas(request):
    bodegas = Bodega.objects.all()
    return render(request, 'bodegas_list.html', {'bodegas': bodegas})

def crear_bodega(request):
    if request.method == 'POST':
        ubicacion = request.POST.get('ubicacion')
        
        Bodega.objects.create(
            ubicacion=ubicacion
        )
        
        messages.success(request, 'Bodega creada exitosamente')
        return redirect('lista_bodegas')
    
    return render(request, 'bodega_form.html')

def editar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    
    if request.method == 'POST':
        bodega.ubicacion = request.POST.get('ubicacion')
        bodega.save()
        
        messages.success(request, 'Bodega actualizada exitosamente')
        return redirect('lista_bodegas')
    
    return render(request, 'bodega_form.html', {'bodega': bodega})

def eliminar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    
    if request.method == 'POST':
        bodega.delete()
        messages.success(request, 'Bodega eliminada exitosamente')
    
    return redirect('lista_bodegas')


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
