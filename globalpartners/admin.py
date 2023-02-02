from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .models import GlobalPartner


@admin.register(GlobalPartner)
class GlobalPartnerAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "patreon_sponsor",
        "sponsor_level_annual",
        "contacted",
        "date_contacted",
        "next_renewal_date",
    )
    list_filter = ("company_name", "contact_person", "patreon_sponsor", "sponsor_level_annual")
    search_fields = ("company_name", "contact_person")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<int:globalpartner_id>/triage/send_prospective_sponsor_email/",
                self.admin_site.admin_view(self.send_prospective_sponsor_email),
                name="globalpartners_globalpartner_send_prospective_sponsor_email",
            ),
            path(
                "<int:globalpartner_id>/triage/send_renewal_email/",
                self.admin_site.admin_view(self.send_renewal_email),
                name="globalpartners_globalpartner_send_renewal_email",
            ),
            path(
                "<int:globalpartner_id>/triage/send_promotional_material_email",
                self.admin_site.admin_view(self.send_promotional_material_email),
                name="globalpartners_globalpartner_send_promotional_material_email",
            ),
            path(
                "<int:globalpartner_id>/triage/send_thank_you_email",
                self.admin_site.admin_view(self.send_thank_you_email),
                name="globalpartners_globalpartner_send_thank_you_email",
            ),
        ]
        return my_urls + urls

    def send_prospective_sponsor_email(self, request, globalpartner_id):
        globalpartner = get_object_or_404(GlobalPartner, id=globalpartner_id)
        globalpartner.send_prospective_sponsor_email()
        messages.success(
            request,
            _("Introduction email for %(contact_person)s, of %(company_name)s has been sent.")
            % {"contact_person": globalpartner.contact_person, "company_name": globalpartner.company_name},
        )

        return redirect("admin:globalpartners_globalpartner_changelist")

    def send_renewal_email(self, request, globalpartner_id):
        globalpartner = get_object_or_404(GlobalPartner, id=globalpartner_id)
        globalpartner.send_renewal_email()
        messages.success(
            request,
            _("Renewal email for %(contact_person)s, of %(company_name)s has been sent.")
            % {"contact_person": globalpartner.contact_person, "company_name": globalpartner.company_name},
        )

        return redirect("admin:globalpartners_globalpartner_changelist")

    def send_promotional_material_email(self, request, globalpartner_id):
        globalpartner = get_object_or_404(GlobalPartner, id=globalpartner_id)
        globalpartner.send_promotional_material_email()
        messages.success(
            request,
            _("Request for promotional material email for %(contact_person)s, of %(company_name)s has been sent.")
            % {"contact_person": globalpartner.contact_person, "company_name": globalpartner.company_name},
        )

        return redirect("admin:globalpartners_globalpartner_changelist")

    def send_thank_you_email(self, request, globalpartner_id):
        globalpartner = get_object_or_404(GlobalPartner, id=globalpartner_id)
        globalpartner.send_thank_you_email()
        messages.success(
            request,
            _("Thank you email for %(contact_person)s, of %(company_name)s has been sent.")
            % {"contact_person": globalpartner.contact_person, "company_name": globalpartner.company_name},
        )

        return redirect("admin:globalpartners_globalpartner_changelist")
