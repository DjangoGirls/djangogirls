from smtplib import SMTPException

from django.core.mail import EmailMessage
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactEmail(models.Model):
    CHAPTER, SUPPORT = "chapter", "support"
    CONTACT_TYPE_CHOICES = (
        (CHAPTER, _("Django Girls Local Organizers")),
        (SUPPORT, _("Django Girls HQ (Support Team)")),
    )

    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    sent_to = models.EmailField(max_length=128)
    message = models.TextField()
    event = models.ForeignKey(
        "core.Event",
        help_text=_("required for contacting a chapter"),
        null=True,
        blank=True,
        on_delete=models.deletion.SET_NULL,
    )
    contact_type = models.CharField(
        verbose_name=_("Who do you want to contact?"), max_length=20, choices=CONTACT_TYPE_CHOICES, default=CHAPTER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_successfully = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.email} to {self.sent_to}"

    def save(self, *args, **kwargs):
        self.sent_to = self._get_to_email()
        email = EmailMessage(
            self._get_subject(),
            self.message,
            "Django Girls Contact <hello@djangogirls.org>",
            [self.sent_to],
            reply_to=[f"{self.name} <{self.email}>"],
            headers={"Reply-To": f"{self.name} <{self.email}>"},
        )
        try:
            email.send(fail_silently=False)
        except SMTPException:
            self.sent_successfully = False

        super().save(*args, **kwargs)

    def _get_to_email(self):
        if self.event and self.event.email:
            return self.event.email
        return "hello@djangogirls.org"

    def _get_subject(self):
        return f"{self.name} - from the djangogirls.org website"
