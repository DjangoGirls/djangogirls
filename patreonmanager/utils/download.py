"""
Download your monthly patron reports from Patreon (CSV).

Requires requests and lxml.
"""
import logging
import re
from datetime import datetime
from urllib.parse import parse_qs, urlparse

import requests
from lxml import html

LOGIN_URL = "https://api.patreon.com/login"

BASE_URL = "https://www.patreon.com"
MANAGER_URL = BASE_URL + "/manageRewards"
MONTH_CSV_DOWNLOAD_URL = BASE_URL + "/downloadCsv"

MONTH_CONTAINER_XPATH = '//div[@id="boxGrid"]/div[@class="box mylink"]'
MONTH_LINK_XPATH = './/div[@class="pledge"]/a'
MONTH_TITLE_RE = re.compile("^(?P<month_year>.+) Patreon supported$")
# In November 2015 the title changed:
NEW_MONTH_TITLE_RE = re.compile("^(?P<month_year>.+) patron supported$")

FILENAME_FORMAT = "{:%Y-%m}-Patreon.csv"


def login(email, password):
    """
    Log in to patreon.com using the given username/password.
    Return a session object with all the right cookies set.
    """
    logging.info("Attempting login with email %r...", email)
    session = requests.session()
    response = session.post(LOGIN_URL, json={"data": {"email": email, "password": password}})
    assert response.status_code == 200
    logging.info("Login successful!")
    # TODO: handle bad username/password
    return session


def gen_monthly_report_links(session):
    """
    Generate download links to the current sessions's monthly CSV reports.
    """
    logging.info("Opening patron manager page...")
    response = session.get(MANAGER_URL)
    assert response.status_code == 200
    logging.info("Done.")

    tree = html.fromstring(response.text)
    containers = tree.xpath(MONTH_CONTAINER_XPATH)
    logging.info("Found %d result(s)", len(containers))

    for container in containers:
        container.make_links_absolute(BASE_URL)
        anchor_node = container.xpath(MONTH_LINK_XPATH)[0]

        hid = _get_hid_from_url(anchor_node.attrib["href"])
        month_datetime = _get_datetime_from_title(anchor_node.text_content())

        filename = FILENAME_FORMAT.format(month_datetime)

        url = _get_full_url(MONTH_CSV_DOWNLOAD_URL, params={"hid": hid})

        yield filename, url


def _get_full_url(url, params):
    """
    Combined the given URL and query parameters into a final URL string.
    """
    r = requests.Request("GET", url, params=params)
    return r.prepare().url


def _get_hid_from_url(url):
    """
    Return the hid (Patreon's month report ID) parameter of the given URL.
    """
    parsed_url = urlparse(url)
    parsed_query = parse_qs(parsed_url.query)
    return parsed_query.get("hid")


def _get_datetime_from_title(title):
    match = NEW_MONTH_TITLE_RE.search(title.strip())
    try:
        assert match is not None
    except:
        match = MONTH_TITLE_RE.search(title.strip())
        assert match is not None

    date_format = "%B %Y"
    return datetime.strptime(match.group("month_year"), date_format)


def _download(session, url, filename):
    """
    Download the file at the given URL and save it to the given filename.

    To save to a different folder, simply include the path in the filename.
    This reads the whole file into memory so it's not suitable for really big
    files.
    """
    logging.info("Downloading file at %r...", url)
    response = session.get(url)
    assert response.status_code == 200
    logging.info("Downloaded!")

    logging.info("Writing downloaded file to %r...", filename)
    with open(filename, "wb") as f:
        f.write(response.content)
    logging.info("File written!")
