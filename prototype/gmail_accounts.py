import string
from httplib2 import Http
from random import choice

from apiclient.errors import HttpError
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


PASSWORD_CHARS = string.ascii_letters + string.digits

def generate_password(length=10):
    return ''.join([choice(PASSWORD_CHARS) for i in range(length)])



"""
Several things were needed to get this working:
1. Create an app in Developer Console
2. Create a service account to enable 2 legged oauth (https://developers.google.com/identity/protocols/OAuth2ServiceAccount)
3. Enable delegation of domain-wide authority for the service account.
4. Enable Admin SDK for the domain.
5. Give the service account permission to access admin.directory.users service (https://admin.google.com/AdminHome?chromeless=1#OGX:ManageOauthClients).
"""

SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'djangogirls_website-93134565f52d.json',
    scopes=SCOPES
)

delegated_credentials = credentials.create_delegated('hello@djangogirls.org')
http_auth = delegated_credentials.authorize(Http())

service = build('admin', 'directory_v1', http=http_auth)


def make_email(slug):
    """Get the email address for the given slug"""
    return '%s@djangogirls.org' % slug


def create_account(slug, city_name):
    """
    Create a new account

    e.g. create_account('testcity', 'Test City')
    """
    email = make_email(slug)
    password = generate_password()
    response = service.users().insert(body={
        "primaryEmail": email,
        "name": {
            "fullName": "Django Girls %s" % city_name,
            "givenName": "Django Girls",
            "familyName": city_name,
        },
        "password": password,
    }).execute()

    print('Account %s created with password %s' % (email, password))

    return response


def change_name(old_slug, new_slug):
    """
    Change the name of an account

    e.g. change_name('testcity', 'testcity1')
    """

    old_email = make_email(old_slug)
    new_email = make_email(new_slug)

    response = service.users().patch(
        userKey=old_email,
        body={
            "primaryEmail": new_email,
        },
    ).execute()

    # The old email address is kept as an alias to the new one, but we don't want this.
    service.users().aliases().delete(userKey=new_email, alias=old_email).execute()

    print('Account %s renamed to %s' % (old_email, new_email))

    return response


def get_account(slug):
    """
    Print out details of the given account - just pass in the slug

    e.g. get_account('testcity')
    """
    try:
        print(service.users().get(userKey=make_email(slug)).execute())
    except HttpError:
        pass
