import logging
from dataclasses import dataclass
import datetime
from typing import (
    Any,
    Iterator,
)

import requests
from requests.exceptions import RequestException

from django.conf import settings

from .models import Story


logger = logging.getLogger(__name__)


@dataclass
class RemoteStory:
    url: str
    content_parts: list[dict[str, Any]]
    created: datetime.datetime

    @property
    def text_parts(self) -> list[str]:
        return [
            content_part["text"]
            for content_part in self.content_parts
            if content_part["type"] == "text"
        ]

    @property
    def title(self) -> str:
        return self.text_parts[0]

    @property
    def content(self) -> str:
        return " ".join(self.text_parts[1:])

    @property
    def is_story(self) -> bool:
        return "Your Django Story" in self.title


def parse_tumblr_posts(posts_data: list[dict[str, Any]]) -> Iterator[RemoteStory]:
    for post_data in posts_data:
        yield RemoteStory(
            url=post_data["post_url"],
            content_parts=post_data["content"],
            created=datetime.datetime.utcfromtimestamp(post_data["timestamp"]),
        )


def request_latest_stories_from_tumblr() -> Iterator[RemoteStory]:
    # TODO: probably write a tumblr client if more endpoints
    # get accessed in the future
    blog_base_url = (
        f"{settings.TUMBLR_API_BASE_URL}/blog/{settings.TUMBLR_BLOG_HOSTNAME}"
    )
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
    except RequestException as exc:
        print(exc)
        logger.exception("Exception when requesting tumblr posts")
        return iter(())

    posts_data = response.json()["response"]["posts"]
    return parse_tumblr_posts(posts_data)


def create_missing_stories(remote_stories: list[RemoteStory]) -> int:
    created = 0
    remote_urls = set(remote_story.url for remote_story in remote_stories)
    in_db_urls = set(
        Story.objects.filter(post_url__in=remote_urls).values_list(
            "post_url", flat=True
        )
    )
    to_create_urls = remote_urls.difference(in_db_urls)
    missing_stories = [
        remote_story
        for remote_story in remote_stories
        if remote_story.url in to_create_urls
    ]
    for missing_story in missing_stories:
        # TODO: still missing image from story posts
        story = Story.objects.create(
            post_url=missing_story.url,
            name=missing_story.title,
            content=missing_story.content,
            is_story=missing_story.is_story,
        )
        story.created = missing_story.created
        story.save()
    return created
