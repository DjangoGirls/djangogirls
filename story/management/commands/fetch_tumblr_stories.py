from urllib.parse import urlparse
from urllib.request import urlretrieve

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from core.tumblr_client import request_latest_stories
from story.models import Story


def download_image(url: str) -> tuple[str, File]:
    image_name = urlparse(url).path.split("/")[-1]
    content = urlretrieve(url)
    return image_name, File(open(content[0], "rb"))


class Command(BaseCommand):
    help = "Fetch Django Girls stories from Tumblr blog"

    def handle(self, *args, **options):
        latest_stories = list(request_latest_stories())
        remote_urls = {remote_story.url for remote_story in latest_stories}
        in_db_urls = set(Story.objects.filter(post_url__in=remote_urls).values_list("post_url", flat=True))
        to_create_urls = remote_urls.difference(in_db_urls)
        missing_stories = [remote_story for remote_story in latest_stories if remote_story.url in to_create_urls]
        created = 0
        for missing_story in missing_stories:
            self.stdout.write(f"Fetching {missing_story.title}")
            with transaction.atomic():
                story = Story.objects.create(
                    post_url=missing_story.url,
                    name=missing_story.title,
                    content=missing_story.content,
                    is_story=missing_story.is_story,
                )
                story.created = missing_story.created
                story.save()
                if missing_story.is_story and missing_story.banner_url:
                    story.image.save(*download_image(missing_story.banner_url), save=True)
            created += 1
        self.stdout.write(f"{created} stories loaded and created from Tumblr blog")
