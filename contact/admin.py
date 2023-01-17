from django.contrib import admin

from .models import ContactEmail


@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ("name", "sent_to", "event", "created_at", "sent_successfully")
    list_filter = ("sent_to",)
    search_fields = (
        "sent_to",
        "event",
    )
    readonly_fields = (
        "name",
        "email",
        "sent_to",
        "message",
        "event",
        "contact_type",
        "created_at",
        "sent_successfully",
    )
