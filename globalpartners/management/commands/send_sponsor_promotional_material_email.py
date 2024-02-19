from django.core.management.base import BaseCommand

from globalpartners.emails import send_promotional_material_email
from globalpartners.models import GlobalPartner


class Command(BaseCommand):
    help = "Sends emails to sponsors asking them for promotional materials"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        try:
            sponsors = GlobalPartner.objects.exclude(sponsor_level_annual="").filter(
                promotional_materials_requested=False
            )
            for sponsor in sponsors:
                send_promotional_material_email(
                    sponsor.contact_person,
                    sponsor.contact_email,
                    sponsor.prospective_sponsor,
                    sponsor.sponsor_level_annual,
                )
                sponsor.promotional_materials_requested = True
                sponsor.save(update_fields=["promotional_materials_requested"])
        except GlobalPartner.DoesNotExist:
            self.stdout.write(self.style.error("No emails requesting promotional materials to send at this point."))
