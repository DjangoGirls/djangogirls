# -*- encoding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def scored_by_user(application, user):
    return application.is_scored_by_user(user)


@register.simple_tag
def display_sorting_arrow(name, current_order):
    is_reversed = False
    if '-{}'.format(name) == current_order:
        is_reversed = True

    if is_reversed:
        return mark_safe('<a href="?order={}">▼</a>'.format(name))
    else:
        return mark_safe('<a href="?order=-{}">▲</a>'.format(name))
