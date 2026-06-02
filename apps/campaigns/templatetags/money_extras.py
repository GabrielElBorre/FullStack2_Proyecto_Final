from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def moneda_mxn(value):
    """Formato: $1,234.56 MXN"""
    if value is None or value == "":
        return "$0.00 MXN"
    try:
        monto = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return f"${value} MXN"
    return f"${monto:,.2f} MXN"
