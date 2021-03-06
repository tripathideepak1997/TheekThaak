from django import template

register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price

@register.simple_tag()
def total(items):
    sum = 0
    for item in items:
        sum+=item.product.price
    return sum