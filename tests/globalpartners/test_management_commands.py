from datetime import date
from io import StringIO

from django.core.management import call_command

from globalpartners.models import GlobalPartner

today = date.today()


def test_send_prospective_sponsor_email_command(partners, out):
    out = call_command(
        "send_prospective_sponsor_email",
        stdout=out,
        stderr=StringIO(),
    )
    sponsors = GlobalPartner.objects.filter(prospective_sponsor=True, contacted=True)
    assert len(sponsors) == 2


def test_send_sponsor_promotional_material_email_command(partners, out):
    out = call_command("send_sponsor_promotional_material_email", stdout=out, stderr=StringIO())
    sponsors = (
        GlobalPartner.objects.exclude(prospective_sponsor=True)
        .filter(is_active=True)
        .filter(promotional_materials_requested=True)
    )
    assert len(sponsors) == 5
    assert sponsors[0].promotional_materials_requested


def test_send_sponsor_renewal_email_command(partners, out):
    out = call_command("send_sponsor_renewal_email", stdout=out, stderr=StringIO())
    sponsors = (
        GlobalPartner.objects.exclude(prospective_sponsor=True)
        .filter(next_renewal_date__lte=today)
        .filter(patreon_sponsor=False)
        .filter(date_contacted=today)
    )
    assert len(sponsors) == 1
    assert sponsors[0].contacted
    assert sponsors[0].date_contacted == today


def test_send_sponsor_thank_you_email_command(partners, out):
    out = call_command("send_sponsor_thank_you_email", stdout=out, stderr=StringIO())
    sponsors = GlobalPartner.objects.exclude(prospective_sponsor=True).filter(is_active=True)
    assert len(sponsors) == 5
    assert not sponsors[0].contacted
