from urllib.parse import urlparse

from django.template import Library

register = Library()


@register.simple_tag
def build_menu_item_url(menu_url, event_page_url):
    parse_result = urlparse(menu_url)
    if parse_result.netloc:  # A full URI with domain.
        return menu_url
    elif parse_result.path.startswith("/"):  # Absolute path.
        return menu_url
    return f"/{event_page_url}/{menu_url}"
