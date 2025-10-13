from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Producto, Prenda, Bodega, PrendaBodega, MovimientoInventario
from django.forms import ModelForm
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal
from django import forms


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

class PrendaBodegaForm(ModelForm): #Formulario para crear y editar prenda bodega
    class Meta:
        model = PrendaBodega
        fields = ['prenda', 'bodega', 'stock']

def lista_prenda_bodega(request):
    # logica para listar prenda bodega
    prenda_bodegas = (
        PrendaBodega.objects.select_related('prenda', 'bodega', 'prenda__producto').all()
    )
    return render(request, 'prenda_bodega_list.html', {'prenda_bodegas': prenda_bodegas})

def crear_prenda_bodega(request):
    if request.method == 'POST':
        form = PrendaBodegaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_prenda_bodega')
    else:
        form = PrendaBodegaForm()
    # logica para crear prenda bodega
    return render(request, 'prenda_bodega_form.html', {'form': form})

def editar_prenda_bodega(request, id):
    pb = get_object_or_404(PrendaBodega, pk=id)
    if request.method == 'POST':
        form = PrendaBodegaForm(request.POST, instance=pb)
        if form.is_valid():
            form.save() 
            return redirect('lista_prenda_bodega')
    else:
        form = PrendaBodegaForm(instance=pb)
    # logica para editar prenda bodega
    return render(request, 'prenda_bodega_form.html', {'form': form})

def eliminar_prenda_bodega(request, id):
    pb = get_object_or_404(PrendaBodega, pk=id)
    pb.delete()
    # logica para eliminar prenda bodega
    return redirect('lista_prenda_bodega')


class MovimientoForm(ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["prenda_bodega", "cantidad", "motivo"]

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad is None or cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad

class MovimientoAddForm(forms.Form):
    """Formulario extendido para crear Prenda y PrendaBodega cuando el motivo es ADD.
    No requiere autenticación en esta iteración.
    """
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), required=True)
    talla = forms.CharField(max_length=10, required=True)
    color = forms.CharField(max_length=30, required=True)
    precio_compra = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    precio_venta = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    bodega = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=True)
    cantidad = forms.IntegerField(min_value=1, required=True)
    motivo = forms.ChoiceField(choices=MovimientoInventario.MOTIVO_CHOICES, required=True)

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo != 'ADD':
            raise ValidationError('Este formulario extendido es solo para motivo ADD.')
        return motivo

"""
NOTA: En esta primera iteración NO se exige login ni autorización para movimientos.
Se asignará un usuario por defecto (primer usuario) al crear/editar movimientos.
"""

# Movimientos CRUD
def lista_movimientos(request):
    movimientos = (
        MovimientoInventario.objects
        .select_related(
            'prenda_bodega',
            'prenda_bodega__prenda',
            'prenda_bodega__bodega',
            'prenda_bodega__prenda__producto'
        )
        .order_by('-fecha')
    )
    return render(request, 'movimientos_list.html', {'movimientos': movimientos})

def _signed_effect(motivo: str, cantidad: int) -> int:
    if motivo == 'ADD':
        return cantidad
    if motivo == 'SELL':
        return -cantidad
    if motivo == 'RETURN':
        return cantidad
    return 0

def crear_movimiento(request):
    # Primera iteración: sin login requerido
    if request.method == 'POST':
        # Dos flujos:
        # - Estándar (usa prenda_bodega existente) -> MovimientoForm
        # - Extendida (crea Prenda y PrendaBodega cuando motivo=ADD) -> MovimientoAddForm
        usar_extendido = request.POST.get('usar_extendido') == '1' or (
            request.POST.get('motivo') == 'ADD' and not request.POST.get('prenda_bodega')
        )
        if usar_extendido:
            add_form = MovimientoAddForm(request.POST)
            if add_form.is_valid():
                producto = add_form.cleaned_data['producto']
                talla = add_form.cleaned_data['talla']
                color = add_form.cleaned_data['color']
                precio_compra = add_form.cleaned_data['precio_compra']
                precio_venta = add_form.cleaned_data['precio_venta']
                bodega = add_form.cleaned_data['bodega']
                cantidad = add_form.cleaned_data['cantidad']
                motivo = add_form.cleaned_data['motivo']  # debe ser 'ADD'

                with transaction.atomic():
                    # Crear Prenda y PrendaBodega
                    prenda = Prenda.objects.create(
                        producto=producto,
                        talla=talla,
                        color=color,
                        precio_compra=precio_compra,
                        precio_venta=precio_venta,
                    )
                    pb = PrendaBodega.objects.create(
                        prenda=prenda,
                        bodega=bodega,
                        stock=0,
                    )

                    # Aplicar efecto (ADD suma cantidad)
                    effect = _signed_effect(motivo, cantidad)
                    pb.stock = pb.stock + effect
                    pb.save(update_fields=['stock'])

                    # Registrar movimiento
                    user = request.user if getattr(request.user, 'is_authenticated', False) else User.objects.first()
                    mov = MovimientoInventario.objects.create(
                        prenda_bodega=pb,
                        cantidad=cantidad,
                        usuario=user,
                        motivo=motivo,
                    )
                    return redirect('lista_movimientos')
            # Si no es válido, continuar al render con ambos forms
            form = MovimientoForm()  # para que el template tenga ambos
        else:
            form = MovimientoForm(request.POST)
            if form.is_valid():
                motivo = form.cleaned_data['motivo']
                cantidad = form.cleaned_data['cantidad']
                pb = form.cleaned_data['prenda_bodega']

            # REGLA: Movimiento afecta tanto a Prenda como a PrendaBodega.
            # - ADD: puede crear Prenda y PrendaBodega (si el formulario extendido entrega datos).
            # - SELL: descuenta stock.
            # - RETURN: suma stock.
            

            effect = _signed_effect(motivo, cantidad)
            with transaction.atomic():
                # Afecta PrendaBodega
                pb_locked = PrendaBodega.objects.select_for_update().get(pk=pb.pk)
                nuevo_stock = pb_locked.stock + effect
                if nuevo_stock < 0:
                    form.add_error(None, 'No hay stock suficiente para realizar la operación.')
                else:
                    # Usuario por defecto si no hay autenticación
                    user = request.user if getattr(request.user, 'is_authenticated', False) else User.objects.first()
                    mov = form.save(commit=False)
                    mov.usuario = user
                    mov.save()

                    pb_locked.stock = nuevo_stock
                    pb_locked.save(update_fields=['stock'])

                    # TODO (cuando Prenda tenga 'stock'): actualizar stock de Prenda según motivo
                    # if hasattr(pb_locked.prenda, 'stock'):
                    #     if motivo == 'ADD' or motivo == 'RETURN':
                    #         pb_locked.prenda.stock = pb_locked.prenda.stock + cantidad
                    #     elif motivo == 'SELL':
                    #         pb_locked.prenda.stock = max(0, pb_locked.prenda.stock - cantidad)
                    #     pb_locked.prenda.save(update_fields=['stock'])
                    return redirect('lista_movimientos')
    else:
        form = MovimientoForm()
        add_form = MovimientoAddForm(initial={'motivo': 'ADD'})
    # Pasamos ambos forms; el template actual puede empezar mostrando uno
    context = {
        'form': form,
        'add_form': add_form if 'add_form' in locals() else MovimientoAddForm(initial={'motivo': 'ADD'})
    }
    return render(request, 'movimiento_form.html', context)

def editar_movimiento(request, id):
    # Primera iteración: sin login requerido
    movimiento = get_object_or_404(MovimientoInventario, pk=id)
    if request.method == 'POST':
        form = MovimientoForm(request.POST, instance=movimiento)
        if form.is_valid():
            nuevo_pb = form.cleaned_data['prenda_bodega']
            nueva_cantidad = form.cleaned_data['cantidad']
            nuevo_motivo = form.cleaned_data['motivo']

            prev_effect = _signed_effect(movimiento.motivo, movimiento.cantidad)
            new_effect = _signed_effect(nuevo_motivo, nueva_cantidad)

            with transaction.atomic():
                if movimiento.prenda_bodega_id != nuevo_pb.id:
                    # Revertir efecto en ubicación anterior
                    old_pb = PrendaBodega.objects.select_for_update().get(pk=movimiento.prenda_bodega_id)
                    old_new_stock = old_pb.stock - prev_effect
                    if old_new_stock < 0:
                        form.add_error(None, 'La edición dejaría stock negativo en la ubicación original.')
                        return render(request, 'movimiento_form.html', {'form': form})
                    old_pb.stock = old_new_stock
                    old_pb.save(update_fields=['stock'])

                    # Aplicar en la nueva ubicación
                    new_pb_locked = PrendaBodega.objects.select_for_update().get(pk=nuevo_pb.pk)
                    new_new_stock = new_pb_locked.stock + new_effect
                    if new_new_stock < 0:
                        form.add_error(None, 'La edición dejaría stock negativo en la nueva ubicación.')
                        return render(request, 'movimiento_form.html', {'form': form})

                    mov = form.save(commit=False)
                    mov.usuario = (request.user if getattr(request.user, 'is_authenticated', False) else User.objects.first())
                    mov.save()

                    new_pb_locked.stock = new_new_stock
                    new_pb_locked.save(update_fields=['stock'])
                    # TODO actualizar también stock de Prenda cuando exista
                    return redirect('lista_movimientos')
                else:
                    # Misma ubicación: aplicar delta neto
                    pb_locked = PrendaBodega.objects.select_for_update().get(pk=movimiento.prenda_bodega_id)
                    nuevo_stock = pb_locked.stock - prev_effect + new_effect
                    if nuevo_stock < 0:
                        form.add_error(None, 'La edición dejaría stock negativo.')
                    else:
                        mov = form.save(commit=False)
                        mov.usuario = (request.user if getattr(request.user, 'is_authenticated', False) else User.objects.first())
                        mov.save()
                        pb_locked.stock = nuevo_stock
                        pb_locked.save(update_fields=['stock'])
                        # TODO actualizar también stock de Prenda cuando exista
                        return redirect('lista_movimientos')
    else:
        form = MovimientoForm(instance=movimiento)
    return render(request, 'movimiento_form.html', {'form': form})

def eliminar_movimiento(request, id):
    # Primera iteración: sin login requerido
    movimiento = get_object_or_404(MovimientoInventario, pk=id)
    with transaction.atomic():
        pb_locked = PrendaBodega.objects.select_for_update().get(pk=movimiento.prenda_bodega_id)
        revert_effect = -_signed_effect(movimiento.motivo, movimiento.cantidad)
        nuevo_stock = pb_locked.stock + revert_effect
        if nuevo_stock < 0:
            return redirect('lista_movimientos')
        pb_locked.stock = nuevo_stock
        pb_locked.save(update_fields=['stock'])
        movimiento.delete()
        # TODO actualizar también stock de Prenda cuando exista
    return redirect('lista_movimientos')
