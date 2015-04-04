# -*- encoding: utf-8 -*-
from django import template

from applications.models import Score


register = template.Library()

@register.filter
def scored_by_user(value, arg):
    try:
        score = Score.objects.get(application=value, user=arg)
        return True if score.score else False
    except Score.DoesNotExist:
        return False


@register.simple_tag
def display_sorting_arrow(name, current_order):
    is_reversed = False
    if '-{}'.format(name) == current_order:
        is_reversed = True

    if is_reversed:
        return '<a href="?order={}">▼</a>'.format(name)
    else:
        return '<a href="?order=-{}">▲</a>'.format(name)
