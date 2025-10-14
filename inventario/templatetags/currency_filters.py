from django import template

register = template.Library()

@register.filter
def currency_format(value):
    """Formatea un número como moneda con separadores de miles"""
    if value is None:
        return "0"
    
    # Convertir a entero para quitar decimales
    int_value = int(float(value))
    
    # Formatear con separadores de miles usando punto
    return f"{int_value:,}".replace(",", ".")
