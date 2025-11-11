from django.db import migrations
from django.utils import timezone
from datetime import timedelta


def forward_seed_ventas(apps, schema_editor):
    MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')
    PrendaBodega = apps.get_model('inventario', 'PrendaBodega')

    skus = [
        "SEED-POL-BAS",
        "SEED-POL-DEP",
        "SEED-POL-GRA",
        "SEED-POL-OVE",
        "SEED-POL-POLO",
    ]

    now = timezone.now()
    idx = 0
    # Ventas de ejemplo distribuidas en los ultimos ~90 dias
    for pb in PrendaBodega.objects.select_related('prenda__producto').filter(prenda__producto__sku__in=skus):
        idx += 1
        qty = 2 if (idx % 3) else 1
        days = (idx % 85) + 5  # entre 5 y 90 dias atras

        # Crear movimiento SELL
        mov = MovimientoInventario.objects.create(
            prenda_bodega=pb,
            cantidad=qty,
            motivo='SELL',
        )
        # Ajustar fecha para simular historico
        MovimientoInventario.objects.filter(pk=mov.pk).update(fecha=now - timedelta(days=days))
        # Actualizar stock
        pb.stock = max(0, pb.stock - qty)
        pb.save()


def reverse_seed_ventas(apps, schema_editor):
    MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')
    PrendaBodega = apps.get_model('inventario', 'PrendaBodega')

    skus = [
        "SEED-POL-BAS",
        "SEED-POL-DEP",
        "SEED-POL-GRA",
        "SEED-POL-OVE",
        "SEED-POL-POLO",
    ]

    movs = MovimientoInventario.objects.select_related('prenda_bodega__prenda__producto').filter(
        motivo='SELL',
        prenda_bodega__prenda__producto__sku__in=skus
    )
    # Restaurar stock y eliminar solo los movimientos seed
    for m in movs:
        pb = m.prenda_bodega
        pb.stock = pb.stock + m.cantidad
        pb.save()
    movs.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_seed_poleras'),
    ]

    operations = [
        migrations.RunPython(forward_seed_ventas, reverse_seed_ventas),
    ]
