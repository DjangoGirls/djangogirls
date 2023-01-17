import datetime
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


@dataclass
class RemoteStory:
    url: str
    content_parts: list[dict[str, Any]]
    created: datetime.datetime

    @property
    def text_parts(self) -> list[str]:
        return [content_part["text"] for content_part in self.content_parts if content_part["type"] == "text"]

    @property
    def image_parts(self) -> list[dict]:
        return [content_part["media"] for content_part in self.content_parts if content_part["type"] == "image"]

    @property
    def banner_url(self) -> str | None:
        if not self.image_parts:
            return None
        # Each image part has multiple image sizes, we're picking the first
        return self.image_parts[0][0]["url"]

    @property
    def title(self) -> str:
        return self.text_parts[0]

    @property
    def content(self) -> str:
        return " ".join(self.text_parts[1:])

    @property
    def is_story(self) -> bool:
        return "Your Django Story" in self.title


def parse_posts(posts_data: list[dict[str, Any]]) -> Iterator[RemoteStory]:
    for post_data in posts_data:
        yield RemoteStory(
            url=post_data["post_url"],
            content_parts=post_data["content"],
            created=datetime.datetime.utcfromtimestamp(post_data["timestamp"]),
        )


def request_latest_stories() -> Iterator[RemoteStory]:
    # TODO: probably write a wrapper for tumblr requests if
    # more endpoints are used in the future
    blog_base_url = f"{settings.TUMBLR_API_BASE_URL}/blog/{settings.TUMBLR_BLOG_HOSTNAME}"
    posts_endpoint = f"{blog_base_url}/posts/"
    try:
        # `npf` means Neue Post Format - so we don't get different response
        # outputs for legacy versus `NPF` posts
        response = requests.get(
            posts_endpoint,
            params={"api_key": settings.TUMBLR_API_KEY, "npf": True},
            timeout=5,
        )
        response.raise_for_status()
    except RequestException:
        logger.exception("Exception when requesting tumblr posts")
        return iter(())

    posts_data = response.json()["response"]["posts"]
    return parse_posts(posts_data)
