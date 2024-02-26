from datetime import date

from django.core.management.base import BaseCommand

from globalpartners.emails import send_renewal_email
from globalpartners.models import GlobalPartner


class Command(BaseCommand):
    help = "Sends renewal emails to sponsors"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        try:
            sponsors = (
                GlobalPartner.objects.exclude(prospective_sponsor=True)
                .filter(patreon_sponsor=False)
                .filter(contacted=False)
                .filter(next_renewal_date__lte=date.today())
            )
            for sponsor in sponsors:
                send_renewal_email(sponsor.contact_email, sponsor.contact_email)
                sponsor.contacted = True
                sponsor.date_contacted = date.today()
                sponsor.save(update_fields=["contacted", "date_contacted"])
        except GlobalPartner.DoesNotExist:
            self.stdout.write(self.style.error("No sponsor renewal emails to email at this point."))
