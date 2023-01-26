from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ungettext

from .filters import PendingRewardsFilter
from .models import FundraisingStatus, Patron, Payment, Reward


class InlinePaymentAdmin(admin.StackedInline):
    model = Payment
    extra = 1


@admin.register(Patron)
class PatronAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "twitter_link", "since", "uncompleted_payments", "payments_link")
    list_filter = ["since", PendingRewardsFilter]
    search_fields = ["name", "email", "twitter"]
    inlines = (InlinePaymentAdmin,)

    def twitter_link(self, patron):
        if not patron.twitter:
            return ""
        return format_html('<a href="https://twitter.com/{0}">@{0}</a>', patron.twitter)

    twitter_link.short_description = _("Twitter")
    twitter_link.admin_order_field = "twitter"

    def payments_link(self, patron):
        link = reverse("admin:patreonmanager_payment_changelist") + "?patron_id__exact=%s" % patron.pk
        count = patron.payments.count()
        return format_html('<a href="{}">{}</a>', link, ungettext("%d payment", "%d payments", count) % count)

    payments_link.short_description = _("Payments")

    def uncompleted_payments(self, patron):
        count = patron.payments.filter(completed=False).count()
        return format_html("{}", ungettext("%d payment", "%d payments", count) % count)

    uncompleted_payments.short_description = _("Uncompleted payments")


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "value")
    search_fields = ["name"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("get_month_display", "linked_patron", "reward", "pledge", "status", "completed")
    list_filter = ["reward", "status", "completed"]
    list_select_related = ["patron", "reward"]
    date_hierarchy = "month"
    search_fields = ["patron__name", "patron__email", "patron__twitter"]
    ordering = ["month", "patron__name"]
    actions = ["mark_completed"]

    def linked_patron(self, payment):
        link = reverse("admin:patreonmanager_patron_change", args=(payment.patron.pk,))
        return format_html('<a href="{}">{}</a>', link, payment.patron.name)

    linked_patron.short_description = _("Patron")
    linked_patron.admin_order_field = "patron"

    def mark_completed(self, request, queryset):
        updated = queryset.complete()
        msg = ungettext("Marked %d payment as completed", "Marked %d payments as completed", updated)
        messages.success(request, msg % updated)

    mark_completed.short_description = _("Mark selected payments as completed")


@admin.register(FundraisingStatus)
class FundraisingStatusAdmin(admin.ModelAdmin):
    pass
