from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

from core.models import Event

GAPPS_JSON_CREDENTIALS = {
    "type": "service_account",
    "project_id": "djangogirls-website",
    "private_key_id": settings.GAPPS_PRIVATE_KEY_ID,
    "private_key": settings.GAPPS_PRIVATE_KEY.replace("\\n", "\n"),
    "client_email": "django-girls-website@djangogirls-website.iam.gserviceaccount.com",
    "client_id": "114585708723701029855",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/"
    "django-girls-website%40djangogirls-website.iam.gserviceaccount.com",
}


def get_gapps_client():
    if not settings.GAPPS_PRIVATE_KEY or not settings.GAPPS_PRIVATE_KEY_ID:
        return None

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        GAPPS_JSON_CREDENTIALS, scopes=settings.GAPPS_ADMIN_SDK_SCOPES
    )

    delegated_credentials = credentials.create_delegated("hello@djangogirls.org")
    http_auth = delegated_credentials.authorize(Http())

    return build("admin", "directory_v1", http=http_auth)


def make_email(slug):
    """Get the email address for the given slug"""
    return f"{slug}@djangogirls.org"


def create_gmail_account(event):
    """
    Create a new account
    """
    email = event.email
    password = get_random_string(length=10)
    service = get_gapps_client()
    if not service:
        return None, None

    try:
        service.users().insert(
            body={
                "primaryEmail": email,
                "name": {
                    "fullName": event.name,
                    "givenName": "Django Girls",
                    "familyName": event.city,
                },
                "password": password,
                "changePasswordAtNextLogin": True,
            }
        ).execute()
    except HttpError:
        return None, None

    return email, password


def migrate_gmail_account(new_event, slug):
    """
    Change the name of an account
    """
    old_email = make_email(slug)
    old_event = Event.objects.exclude(id=new_event.id).filter(email=old_email).order_by("-id").first()

    if old_event:
        new_email = make_email(slug + str(old_event.date.month) + str(old_event.date.year))
    else:
        new_email = make_email(slug + str(timezone.now().month) + str(timezone.now().year))
    service = get_gapps_client()
    if not service:
        return None

    service.users().patch(
        userKey=old_email,
        body={
            "primaryEmail": new_email,
        },
    ).execute()

    # The old email address is kept as an alias to the new one, but we don't want this.
    service.users().aliases().delete(userKey=new_email, alias=old_email).execute()

    if old_event:
        old_event.email = new_email
        old_event.save()


def get_gmail_account(slug):
    """
    Return the details of the given account - just pass in the slug
    e.g. get_account('testcity')
    """
    service = get_gapps_client()
    if not service:
        return None

    try:
        return service.users().get(userKey=make_email(slug)).execute()
    except HttpError:
        return None


def get_or_create_gmail(event_application, event):
    """
    Function that decides whether Gmail account should be migrated,
    or created. Returns a tuple of email address and password.
    """
    if get_gmail_account(event_application.website_slug) or get_gmail_account(event.page_url):
        # account exists, do we need to migrate?
        if event_application.has_past_team_members(event):
            # has old organizers, so no need to do anything
            return make_email(event_application.website_slug), None
        else:
            # migrate old email
            migrate_gmail_account(event, event_application.website_slug)
            # create new account
            return create_gmail_account(event)
    else:
        # create a new account
        return create_gmail_account(event)
