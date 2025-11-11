from django.db import migrations
from django.contrib.auth.hashers import make_password


def forward_create_demo_and_assign(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')

    # Crear/asegurar usuario demo
    demo, created = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@stockbox.cl',
            'is_active': True,
            'is_staff': True,
        }
    )
    # Asegurar email y password
    demo.email = 'demo@stockbox.cl'
    demo.is_active = True
    demo.is_staff = True
    demo.password = make_password('Demo1234')
    demo.save(update_fields=['email', 'is_active', 'is_staff', 'password'])

    skus = [
        'SEED-POL-BAS',
        'SEED-POL-DEP',
        'SEED-POL-GRA',
        'SEED-POL-OVE',
        'SEED-POL-POLO',
    ]

    # Asignar movimientos seed al usuario demo
    qs = MovimientoInventario.objects.select_related('prenda_bodega__prenda__producto').filter(
        prenda_bodega__prenda__producto__sku__in=skus
    )
    for mov in qs:
        mov.usuario_id = demo.id
        mov.save(update_fields=['usuario'])


def reverse_unassign_demo_from_movements(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    MovimientoInventario = apps.get_model('inventario', 'MovimientoInventario')

    skus = [
        'SEED-POL-BAS',
        'SEED-POL-DEP',
        'SEED-POL-GRA',
        'SEED-POL-OVE',
        'SEED-POL-POLO',
    ]

    try:
        demo = User.objects.get(username='demo', email='demo@stockbox.cl')
    except User.DoesNotExist:
        demo = None

    if demo:
        MovimientoInventario.objects.select_related('prenda_bodega__prenda__producto').filter(
            prenda_bodega__prenda__producto__sku__in=skus,
            usuario=demo
        ).update(usuario=None)
    # No eliminamos el usuario demo por seguridad


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_seed_ventas'),
    ]

    operations = [
        migrations.RunPython(forward_create_demo_and_assign, reverse_unassign_demo_from_movements),
    ]
