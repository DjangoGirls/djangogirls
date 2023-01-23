from django import template

register = template.Library()


@register.simple_tag
def element_by_counter(data, counter, divider):
    if divider == 0:
        return ""
    else:
        index = int(counter / divider)
        if index < len(data):
            return data[index]
    return ""
