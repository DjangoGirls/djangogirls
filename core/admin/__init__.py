from django.contrib import admin
from django.contrib.flatpages.models import FlatPage

from core.admin.event import EventAdmin
from core.admin.event_page_content import EventPageContentAdmin
from core.admin.event_page_menu import EventPageMenuAdmin
from core.admin.flat_page import MyFlatPageAdmin
from core.admin.user import UserAdmin
from core.models import Event, EventPageContent, EventPageMenu, User

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, MyFlatPageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPageContent, EventPageContentAdmin)
admin.site.register(EventPageMenu, EventPageMenuAdmin)
admin.site.register(User, UserAdmin)
