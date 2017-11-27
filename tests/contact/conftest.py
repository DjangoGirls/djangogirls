import os

import pytest


@pytest.fixture(autouse=True)
def recaptcha_testing():
    os.environ['RECAPTCHA_TESTING'] = 'True'