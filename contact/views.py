from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from contact.forms import ContactForm


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = reverse_lazy("contact:landing")

    def form_valid(self, form):
        contact_email = form.save()
        if contact_email.sent_successfully:
            messages.info(self.request, _("Thank you for your email. We will be in touch shortly."))
        else:
            messages.error(self.request, _("Ooops. We couldn't send your email :( Please try again later"))
        return super().form_valid(form)
