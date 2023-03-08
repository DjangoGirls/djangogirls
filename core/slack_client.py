from django.conf import settings
from slack_sdk import WebClient

slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)


def invite_user_to_slack(email, first_name):
    return slack_client.admin_users_invite(
        channel_ids=settings.SLACK_INVITE_CHANNEL_IDS,
        team_id=settings.SLACK_TEAM_ID,
        email=email,
        first_name=first_name,
        set_active=True,
    )


def post_message_to_slack(channel: str, message: str):
    return slack_client.chat_postMessage(
        channel=channel, text=message, username="Django Girls", icon_emoji=":django_heart:"
    )
