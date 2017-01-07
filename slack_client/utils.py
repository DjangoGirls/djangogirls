from django.conf import settings

from slacker import Slacker, Users
from slacker.utils import get_item_id_by_name


def _invite(self, email, **kwargs):
    """
    There's only a private API to invite users to a slack team.
    This function will be monkeypatched onto slacker.User and it seems to work.
    """
    data = dict(email=email, **kwargs)
    channels = data.pop('channels', None)
    if channels is not None:
        data['channels'] = ','.join(_convert_channels(channels))
    return self.post('users.admin.invite', data=data)


def _monkeypatch_user_invite():
    Users.invite = _invite


def get_connection():
    return Slacker(settings.SLACK_API_KEY)


def _convert_channels(channels):
    """
    Convert the given list of channels into thei internal slack IDs, suitable
    for passing to _invite().

    Channel names like #foo get converted to a string like C03PLKT3G.
    """
    connection = get_connection()
    converted = []
    for channel in channels:
        if not channel.startswith('#'):
            converted.append(channel)
            continue
        channel = channel[1:]  # strip leading '#'
        channel_id = connection.channels.get_channel_id(channel)
        if channel_id is None:
            # try a private channel
            private_channels = connection.groups.list().body['groups']
            channel_id = get_item_id_by_name(private_channels, channel)
        if channel_id is None:
            # TODO: handle error?
            continue
        converted.append(channel_id)

    return converted
