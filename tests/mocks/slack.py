import pytest
from easydict import EasyDict

from core.slack_client import slack_client


@pytest.fixture()
def slack_mock(mocker):
    mocks = EasyDict()

    mocks.chat_postMessage = mocker.patch.object(slack_client, 'chat_postMessage')
    mocks.admin_users_invite = mocker.patch.object(slack_client, 'admin_users_invite')

    return mocks
