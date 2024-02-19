from datetime import date

from django.core.management.base import BaseCommand

from globalpartners.emails import send_thank_you_email
from globalpartners.models import GlobalPartner


class Command(BaseCommand):
    help = "Sends thank you emails to sponsors at the end of the year"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        today = date.today()
        year = date.year()
        if today == f"12/12/{year}":
            try:
                sponsors = GlobalPartner.objects.exclude(sponsor_level_annual="").filter(is_displayed=True)
                for sponsor in sponsors:
                    send_thank_you_email(sponsor.contact_person, sponsor.contact_email)
                    sponsor.contacted = False
                    sponsor.save(update_fields=["contacted"])
            except GlobalPartner.DoesNotExist:
                self.stdout.write(self.style.error("No sponsor renewal emails to email at this point."))
