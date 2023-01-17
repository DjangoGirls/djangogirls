from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def display_sorting_arrow(name, current_order):
    is_reversed = False
    if f"-{name}" == current_order:
        is_reversed = True

    if is_reversed:
        return mark_safe(f'<a href="?order={name}">▼</a>')
    else:
        return mark_safe(f'<a href="?order=-{name}">▲</a>')
