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
