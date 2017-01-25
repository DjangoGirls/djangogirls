from django.contrib import messages
from django.views.generic.edit import FormView

from contact.forms import ContactForm


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact/contact.html"

    def form_valid(self, form):
        contact_email = form.save()
        if contact_email.sent_successfully:
            messages.info(
                self.request, "Thank you for your email. We will be in touch shortly."
            )
        else:
            messages.error(
                self.request, "Ooops. We couldn't send your email :( Please try again later"
            )
