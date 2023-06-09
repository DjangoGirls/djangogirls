from datetime import date

from django.template.loader import render_to_string

from core.emails import send_email

year = date.year


def send_sponsor_email(contact_person, contact_email, template, subject, errors=None):
    content = render_to_string(template, {"contact_person": contact_person, "errors": errors})

    send_email(content, subject, [contact_email])


def send_prospective_sponsor_email(contact_person, contact_email):
    """Sends email to prospective sponsor asking the if they are interested
    sponsoring Django Girls Foundation."""
    subject = "Django Girls Foundation Sponsorship"
    template = "emails/globalpartners/prospective_sponsor.html"
    send_sponsor_email(contact_person, contact_email, template, subject)


def send_renewal_email(contact_person, contact_email):
    """Sends annual sponsors email asking if they are interested in supporting
    our work in the new year.
    """
    subject = "Will you be supporting us again in 2023?"
    template = "emails/globalpartners/renewal_email.html"
    send_sponsor_email(contact_person, contact_email, template, subject)


def send_promotional_material_email(
    contact_person, contact_email, prospective_sponsor, sponsor_level_annual, errors=None
):
    """Sends new sponsors/patreon sponsors asking them for materials to use in
    announcing/promoting the sponsor."""
    subject = "Promotional material for our social media and blog"
    template = "emails/globalpartners/promotional_material.html"
    content = render_to_string(
        template,
        {
            "contact_person": contact_person,
            "prospective_sponsor": prospective_sponsor,
            "sponsor_level": sponsor_level_annual,
            "errors": errors,
        },
    )
    send_email(content, subject, [contact_email])


def send_thank_you_email(contact_person, contact_email):
    """Sends thank you email to all sponsors thanking them for supporting our work
    for the year.
    """
    subject = "Thank you for supporting our work"
    template = "emails/globalpartners/thank_you.html"
    send_sponsor_email(contact_person, contact_email, template, subject)
