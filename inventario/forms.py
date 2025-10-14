from django import forms
from .models import Producto, Prenda, Bodega, PrendaBodega, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'sku', 'categoria', 'marca', 'proveedor',
            'descripcion', 'precio_compra', 'precio_venta', 'stock_minimo',
            'estado', 'genero', 'imagen'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PrendaForm(forms.ModelForm):
    # Campos adicionales para bodega y stock
    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Bodega *'
    )
    stock_inicial = forms.IntegerField(
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Stock Inicial *'
    )
    
    class Meta:
        model = Prenda
        fields = ['producto', 'talla', 'color']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'talla': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opciones de tallas
        TALLA_CHOICES = [
            ('', 'Seleccionar talla'),
            ('XS', 'XS'),
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
        ]
        self.fields['talla'].widget.choices = TALLA_CHOICES
        
        # Opciones de colores
        COLOR_CHOICES = [
            ('', 'Seleccionar color'),
            ('Negro', 'Negro'),
            ('Blanco', 'Blanco'),
            ('Gris', 'Gris'),
            ('Azul', 'Azul'),
            ('Rojo', 'Rojo'),
            ('Verde', 'Verde'),
            ('Amarillo', 'Amarillo'),
            ('Rosa', 'Rosa'),
            ('Morado', 'Morado'),
            ('Café', 'Café'),
            ('Otro', 'Otro'),
        ]
        self.fields['color'].widget = forms.Select(attrs={'class': 'form-select'})
        self.fields['color'].widget.choices = COLOR_CHOICES


class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['ubicacion']
        widgets = {
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ubicacion'].widget.attrs.update({
            'placeholder': 'Ej: Bodega Principal, Almacén Norte, etc.'
        })


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['prenda_bodega', 'cantidad', 'motivo']
        widgets = {
            'prenda_bodega': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar las opciones de prenda_bodega para mostrar información más clara
        self.fields['prenda_bodega'].queryset = PrendaBodega.objects.select_related('prenda__producto', 'bodega').all()
        
        # Personalizar las opciones de motivo
        MOTIVO_CHOICES = [
            ('ADD', 'Entrada (Agregar Stock)'),
            ('SELL', 'Salida (Venta)'),
            ('RETURN', 'Salida (Devolución)'),
        ]
        self.fields['motivo'].widget.choices = MOTIVO_CHOICES
        
        # Personalizar las opciones de prenda_bodega para mostrar información más clara
        choices = []
        for pb in PrendaBodega.objects.select_related('prenda__producto', 'bodega').all():
            choice_text = f"{pb.prenda.producto.nombre} - {pb.prenda.talla} - {pb.prenda.color} en {pb.bodega.ubicacion} (Stock: {pb.stock})"
            choices.append((pb.id, choice_text))
        
        self.fields['prenda_bodega'].widget.choices = [('', 'Seleccionar prenda en bodega...')] + choices
