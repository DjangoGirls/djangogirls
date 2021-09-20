from django.template import Library

from django.utils.six.moves.urllib.parse import urlparse

register = Library()


@register.simple_tag
def build_menu_item_url(menu_url, event_page_url):
    parse_result = urlparse(menu_url)
    if parse_result.netloc:     # A full URI with domain.
        return menu_url
    elif parse_result.path.startswith('/'):     # Absolute path.
        return menu_url
    return '/{}/{}'.format(event_page_url, menu_url)
