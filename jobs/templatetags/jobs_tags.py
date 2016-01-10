from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, new_classes):

    old_classes = field.field.widget.attrs.get('class', '')
    classes = ' '.join([old_classes, new_classes])
    return field.as_widget(attrs={"class": classes})
