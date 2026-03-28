from django import template

register = template.Library()

@register.filter
def widthmultiply(value, arg):
    """Multiply value by arg and divide by another value"""
    try:
        parts = str(arg).split()
        if len(parts) == 2:
            multiplier = float(parts[0])
            divisor = float(parts[1])
            result = (float(value) * multiplier) / divisor
            return round(result, 1)
        return 0
    except:
        return 0
