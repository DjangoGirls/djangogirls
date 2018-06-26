from django import template
register = template.Library()

@register.simple_tag
def element_by_counter(data, counter, divider):
     index = int(counter / divider)
     if index < len(data):
          return data[index]
     return ''