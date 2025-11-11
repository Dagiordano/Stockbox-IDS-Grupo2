from django.db import migrations
from decimal import Decimal


def forward_seed_poleras(apps, schema_editor):
    Producto = apps.get_model('inventario', 'Producto')
    Prenda = apps.get_model('inventario', 'Prenda')
    Bodega = apps.get_model('inventario', 'Bodega')
    PrendaBodega = apps.get_model('inventario', 'PrendaBodega')

    bodega, _ = Bodega.objects.get_or_create(ubicacion="Bodega Principal")

    # Precios ajustados a CLP (pesos chilenos)
    categorias = [
        ("Basicas",    "SEED-POL-BAS",  "Algodon 100%",      Decimal("5000.00"),  Decimal("7990.00")),
        ("Deportivas", "SEED-POL-DEP",  "Poliester Dry-Fit", Decimal("7000.00"),  Decimal("12990.00")),
        ("Graficas",   "SEED-POL-GRA",  "Algodon peinado",   Decimal("6500.00"),  Decimal("11990.00")),
        ("Oversize",   "SEED-POL-OVE",  "Algodon pesado",    Decimal("8000.00"),  Decimal("14990.00")),
        ("Polo",       "SEED-POL-POLO", "Algodon Pique",     Decimal("9000.00"),  Decimal("16990.00")),
    ]

    tallas = ["XS", "S", "M", "L", "XL"]
    colores = ["Blanco", "Negro", "Gris", "Azul", "Rojo"]

    for categoria, sku, material, pcompra, pventa in categorias:
        producto, _ = Producto.objects.get_or_create(
            sku=sku,
            defaults={
                "nombre": f"Polera {categoria}",
                "categoria": categoria,
                "marca": "StockBox",
                "material": material,
                "estado": "nuevo",
                "genero": "unisex",
                "descripcion": "Semilla automatica de categorias de poleras",
                "proveedor": "Proveedor Demo",
                "stock_minimo": 5,
            },
        )

        for i, talla in enumerate(tallas):
            color = colores[i % len(colores)]
            prenda, _ = Prenda.objects.get_or_create(
                producto=producto,
                talla=talla,
                color=color,
                defaults={
                    "precio_compra": pcompra,
                    "precio_venta": pventa,
                },
            )

            PrendaBodega.objects.get_or_create(
                prenda=prenda,
                bodega=bodega,
                defaults={"stock": 10},
            )


def reverse_seed_poleras(apps, schema_editor):
    Producto = apps.get_model('inventario', 'Producto')
    Prenda = apps.get_model('inventario', 'Prenda')
    PrendaBodega = apps.get_model('inventario', 'PrendaBodega')

    skus = [
        "SEED-POL-BAS",
        "SEED-POL-DEP",
        "SEED-POL-GRA",
        "SEED-POL-OVE",
        "SEED-POL-POLO",
    ]

    for sku in skus:
        try:
            producto = Producto.objects.get(sku=sku)
        except Producto.DoesNotExist:
            continue
        prendas = Prenda.objects.filter(producto=producto)
        PrendaBodega.objects.filter(prenda__in=prendas).delete()
        prendas.delete()
        producto.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_move_precio_to_prenda'),
    ]

    operations = [
        migrations.RunPython(forward_seed_poleras, reverse_seed_poleras),
    ]
