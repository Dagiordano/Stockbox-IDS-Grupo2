from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import json
from .models import Producto, Prenda, Bodega, PrendaBodega, MovimientoInventario
from .forms import ProductoForm, PrendaForm, BodegaForm, MovimientoForm


# Create your views here.



def home(request):
    # Si no está autenticado, redirigir al login
    if not request.user.is_authenticated:
        return redirect('account_login')
    return render(request, 'home.html')

# Dashboard
@login_required
def gestionar(request):
    # Vista para seleccionar qué gestionar (productos, prendas, bodegas)
    return render(request, 'gestionar.html')

@login_required
def dashboard(request):
    # Calcular stock total
    total_stock = PrendaBodega.objects.aggregate(total=Sum('stock'))['total'] or 0
    
    # Calcular ventas de los últimos 30 días
    fecha_limite = timezone.now() - timedelta(days=30)
    ventas_ultimo_mes = MovimientoInventario.objects.filter(
        motivo='SELL',
        fecha__gte=fecha_limite
    ).aggregate(total=Sum('cantidad'))['total'] or 0
    
    # Contar total de productos únicos
    total_poleras = Producto.objects.count()
    
    # Contar total de bodegas
    total_bodegas = Bodega.objects.count()
    
    # Datos para el gráfico de ventas por modelo (últimos 30 días)
    ventas_por_producto = MovimientoInventario.objects.filter(
        motivo='SELL',
        fecha__gte=fecha_limite
    ).values(
        'prenda_bodega__prenda__producto__nombre'
    ).annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido')[:5]
    
    sales_labels = [item['prenda_bodega__prenda__producto__nombre'] for item in ventas_por_producto]
    sales_data = [item['total_vendido'] for item in ventas_por_producto]
    
    # Datos para el gráfico de stock por categoría
    stock_por_categoria = Producto.objects.values('categoria').annotate(
        total_stock=Sum('prenda__prendabodega__stock')
    ).order_by('-total_stock')
    
    stock_labels = [item['categoria'] for item in stock_por_categoria if item['total_stock']]
    stock_data = [item['total_stock'] for item in stock_por_categoria if item['total_stock']]
    
    context = {
        'total_stock': total_stock,
        'total_ventas': ventas_ultimo_mes,
        'total_poleras': total_poleras,
        'total_bodegas': total_bodegas,
        'sales_labels': json.dumps(sales_labels),
        'sales_data': json.dumps(sales_data),
        'stock_labels': json.dumps(stock_labels),
        'stock_data': json.dumps(stock_data),
    }
    
    return render(request, 'dashboard.html', context)



# Productos CRUD
@login_required
def lista_productos(request):
    # logica para listar productos
    productos = Producto.objects.all()
   
    return render(request, 'productos_list.html', {'productos': productos})

@login_required
def crear_producto(request):
    # logica para crear producto
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente')
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    tallas = ["XS", "S", "M", "L", "XL", "XXL"]
    colores = ["Negro", "Blanco", "Gris", "Azul", "Rojo", "Verde", "Amarillo", "Rosa", "Morado", "Café"]

    return render(request, 'producto_form.html', {
        'form': form,
        'tallas': tallas,
        'colores': colores
        })

@login_required
def editar_producto(request, id):
    # logica para editar producto
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    tallas = ["XS", "S", "M", "L", "XL", "XXL"]
    colores = ["Negro", "Blanco", "Gris", "Azul", "Rojo", "Verde", "Amarillo", "Rosa", "Morado", "Café"]

    return render(request, 'producto_form.html', {
        'form': form,
        'tallas': tallas,
        'colores': colores
        })

@login_required
def eliminar_producto(request, id):
    # logica para eliminar producto
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
    
    return redirect('lista_productos')



# Prendas CRUD
@login_required
def lista_prendas(request):
    prendas = Prenda.objects.all().select_related('producto').prefetch_related('prendabodega_set__bodega')
    
    # Calcular total de stock
    total_stock = 0
    for prenda in prendas:
        for pb in prenda.prendabodega_set.all():
            total_stock += pb.stock
    
    return render(request, 'prendas_list.html', {
        'prendas': prendas,
        'total_stock': total_stock
    })

@login_required
def crear_prenda(request):
    if request.method == 'POST':
        form = PrendaForm(request.POST)
        if form.is_valid():
            # Guardar la prenda
            prenda = form.save()
            
            # Crear la relación PrendaBodega con el stock inicial
            bodega = form.cleaned_data['bodega']
            stock_inicial = form.cleaned_data['stock_inicial']
            
            PrendaBodega.objects.create(
                prenda=prenda,
                bodega=bodega,
                stock=stock_inicial
            )
            
            messages.success(request, 'Prenda creada exitosamente')
            return redirect('lista_prendas')
    else:
        form = PrendaForm()

    return render(request, 'prenda_form.html', {'form': form})

@login_required
def editar_prenda(request, id):
    prenda = get_object_or_404(Prenda, id=id)
    
    if request.method == 'POST':
        form = PrendaForm(request.POST, instance=prenda)
        if form.is_valid():
            # Solo guardar los datos básicos de la prenda
            # Los campos de bodega y stock_inicial no se procesan en edición
            prenda.producto = form.cleaned_data['producto']
            prenda.talla = form.cleaned_data['talla']
            prenda.color = form.cleaned_data['color']
            prenda.save()
            
            messages.success(request, 'Prenda actualizada exitosamente')
            return redirect('lista_prendas')
    else:
        form = PrendaForm(instance=prenda)
    
    return render(request, 'prenda_form.html', {'form': form, 'prenda': prenda})

@login_required
def eliminar_prenda(request, id):
    prenda = get_object_or_404(Prenda, id=id)
    
    if request.method == 'POST':
        prenda.delete()
        messages.success(request, 'Prenda eliminada exitosamente')
    
    return redirect('lista_prendas')




# Bodegas CRUD
@login_required
def lista_bodegas(request):
    bodegas = Bodega.objects.all()
    return render(request, 'bodegas_list.html', {'bodegas': bodegas})

@login_required
def crear_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega creada exitosamente')
            return redirect('lista_bodegas')
    else:
        form = BodegaForm()
    
    return render(request, 'bodega_form.html', {'form': form})

@login_required
def editar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    
    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega actualizada exitosamente')
            return redirect('lista_bodegas')
    else:
        form = BodegaForm(instance=bodega)
    
    return render(request, 'bodega_form.html', {'form': form, 'bodega': bodega})

@login_required
def eliminar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    
    if request.method == 'POST':
        bodega.delete()
        messages.success(request, 'Bodega eliminada exitosamente')
    
    return redirect('lista_bodegas')


# PrendaBodega CRUD
@login_required
def lista_prenda_bodega(request):
    items_stock = PrendaBodega.objects.select_related('prenda__producto', 'bodega').order_by('bodega__ubicacion', 'prenda__producto__nombre')
    return render(request, 'prenda_bodega_list.html', {'items_stock': items_stock})

@login_required
def crear_prenda_bodega(request):
    # logica para crear prenda bodega
    return render(request, 'prenda_bodega_form.html')

@login_required
def editar_prenda_bodega(request, id):
    # logica para editar prenda bodega
    return render(request, 'prenda_bodega_form.html')

@login_required
def eliminar_prenda_bodega(request, id):
    # logica para eliminar prenda bodega
    return render(request, 'prenda_bodega_list.html')



# Movimientos CRUD
@login_required
def lista_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related('prenda_bodega__prenda__producto', 'usuario').order_by('-fecha')
    return render(request, 'movimientos_list.html', {'movimientos': movimientos})

@login_required
def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            
            # Solo asignar usuario si está autenticado
            if request.user.is_authenticated:
                movimiento.usuario = request.user
            # Si no está autenticado, el campo usuario quedará como None (null)
            
            movimiento.save()
            
            # Validar que no se pueda sacar más stock del disponible
            prenda_bodega = movimiento.prenda_bodega
            if movimiento.motivo in ['SELL', 'RETURN']:
                if prenda_bodega.stock < movimiento.cantidad:
                    messages.error(request, f'No hay suficiente stock. Disponible: {prenda_bodega.stock} unidades')
                    return render(request, 'movimiento_form.html', {'form': form})
            
            # Actualizar el stock en PrendaBodega
            if movimiento.motivo == 'ADD':
                prenda_bodega.stock += movimiento.cantidad
            elif movimiento.motivo in ['SELL', 'RETURN']:
                prenda_bodega.stock -= movimiento.cantidad
            prenda_bodega.save()
            
            messages.success(request, 'Movimiento de inventario creado exitosamente')
            return redirect('lista_movimientos')
    else:
        form = MovimientoForm()
    
    return render(request, 'movimiento_form.html', {'form': form})

@login_required
def editar_movimiento(request, id):
    # logica para editar movimiento
    return render(request, 'movimiento_form.html')

@login_required
def eliminar_movimiento(request, id):
    # logica para eliminar movimiento
    return render(request, 'movimientos_list.html')
