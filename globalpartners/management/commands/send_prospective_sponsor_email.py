from datetime import date

from django.core.management.base import BaseCommand

from globalpartners.emails import send_prospective_sponsor_email
from globalpartners.models import GlobalPartner


class Command(BaseCommand):
    help = "Sends emails to prospective sponsors"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        try:
            prospective_sponsors = GlobalPartner.objects.exclude(prospective_sponsor=False).filter(contacted=False)
            for sponsor in prospective_sponsors:
                send_prospective_sponsor_email(sponsor.contact_person, sponsor.contact_email)
                sponsor.contacted = True
                sponsor.date_contacted = date.today()
                sponsor.save(update_fields=["contacted", "date_contacted"])
        except GlobalPartner.DoesNotExist:
            self.stdout.write(self.style.error("No prospective sponsors to email at this point."))
