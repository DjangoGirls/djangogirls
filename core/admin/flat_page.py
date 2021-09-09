from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.forms import CharField


class MyFlatPageAdmin(FlatPageAdmin):

    class MyFlatpageForm(FlatpageForm):
        template_name = CharField(
            initial='flatpage.html',
            help_text="Change this only if you know what you are doing"
        )

    form = MyFlatpageForm
