from typing import Any
from unittest import mock

from requests.exceptions import RequestException

from core import tumblr_client


def test_remote_story_text_parts(remote_story: tumblr_client.RemoteStory):
    assert len(remote_story.text_parts) == 2
    assert remote_story.text_parts[0] == "This is a story text"
    assert remote_story.text_parts[1] == "This is another story text"


def test_remote_story_image_parts(remote_story: tumblr_client.RemoteStory):
    assert len(remote_story.image_parts) == 1
    assert remote_story.image_parts[0][0]["url"] == "/media-small"
    assert remote_story.image_parts[0][1]["url"] == "/media-large"


def test_remote_story_banner_url_no_image_parts(
    remote_story: tumblr_client.RemoteStory,
):
    remote_story.content_parts = []
    assert remote_story.banner_url is None


def test_remote_story_banner_url(
    remote_story: tumblr_client.RemoteStory,
):
    assert remote_story.banner_url == "/media-small"


def test_remote_story_title(
    remote_story: tumblr_client.RemoteStory,
):
    assert remote_story.title == "This is a story text"


def test_remote_story_content(
    remote_story: tumblr_client.RemoteStory,
):
    assert remote_story.content == "This is another story text"


def test_remote_story_is_story_not_story(
    remote_story: tumblr_client.RemoteStory,
):
    assert not remote_story.is_story


def test_remote_story_is_story_story(
    remote_story: tumblr_client.RemoteStory,
):
    remote_story.content_parts[0] = {"type": "text", "text": "Your Django Story"}
    assert remote_story.is_story


def test_parse_posts_no_post_data():
    assert len(list(tumblr_client.parse_posts([]))) == 0


def test_parse_posts():
    posts_data: list[dict[str, Any]] = [
        {
            "post_url": "tumblr.com/stories/1",
            "content": [
                {"type": "text", "text": "Hello"},
                {"type": "text", "text": "there"},
            ],
            "timestamp": 1663437643,
        }
    ]
    remote_story = next(tumblr_client.parse_posts(posts_data))
    assert isinstance(remote_story, tumblr_client.RemoteStory)


@mock.patch("requests.get")
@mock.patch("core.tumblr_client.logger.exception")
def test_request_latest_stories_exception(p_logger_exception, p_get):
    p_get.side_effect = RequestException()
    assert len(list(tumblr_client.request_latest_stories())) == 0
    p_logger_exception.assert_called_once_with("Exception when requesting tumblr posts")


@mock.patch("requests.get")
def test_request_latest_stories(p_get):
    response = mock.Mock()
    response.json = lambda: {"response": {"posts": []}}
    p_get.return_value = response
    assert len(list(tumblr_client.request_latest_stories())) == 0
