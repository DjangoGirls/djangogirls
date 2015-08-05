# -*- encoding: utf-8 -*-
from django import template


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
        return '<a href="?order={}">▼</a>'.format(name)
    else:
        return '<a href="?order=-{}">▲</a>'.format(name)
