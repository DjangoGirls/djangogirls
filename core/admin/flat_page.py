from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.forms import CharField
from django.utils.translation import gettext_lazy as _


class MyFlatPageAdmin(FlatPageAdmin):
    class MyFlatpageForm(FlatpageForm):
        template_name = CharField(
            initial="flatpage.html", help_text=_("Change this only if you know what you are doing")
        )

    form = MyFlatpageForm
