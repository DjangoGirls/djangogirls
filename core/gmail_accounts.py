from httplib2 import Http

from django.conf import settings
from django.utils.crypto import get_random_string
from apiclient.errors import HttpError
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    settings.GOOGLE_APPS_ADMIN_SDK_CREDENTIALS,
    scopes=settings.GOOGLE_APPS_ADMIN_SDK_SCOPES
)

delegated_credentials = credentials.create_delegated('hello@djangogirls.org')
http_auth = delegated_credentials.authorize(Http())

service = build('admin', 'directory_v1', http=http_auth)


def make_email(slug):
    """Get the email address for the given slug"""
    return '%s@djangogirls.org' % slug


def create_account(event):
    """
    Create a new account

    e.g. create_account('testcity', 'Test City')
    """
    email = event.email
    password = get_random_string(length=10)
    service.users().insert(body={
        "primaryEmail": email,
        "name": {
            "fullName": event.name,
            "givenName": "Django Girls",
            "familyName": event.city,
        },
        "password": password,
    }).execute()

    return (email, password)


def change_name(old_slug, new_slug):
    """
    Change the name of an account
    e.g. change_name('testcity', 'testcity1')
    """
    old_email = make_email(old_slug)
    new_email = make_email(new_slug)

    service.users().patch(
        userKey=old_email,
        body={
            "primaryEmail": new_email,
        },
    ).execute()

    # The old email address is kept as an alias to the new one, but we don't want this.
    service.users().aliases().delete(userKey=new_email, alias=old_email).execute()


def get_account(slug):
    """
    Return the details of the given account - just pass in the slug
    e.g. get_account('testcity')
    """
    try:
        return service.users().get(userKey=make_email(slug)).execute()
    except HttpError:
        pass
