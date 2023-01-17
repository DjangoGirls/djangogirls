from unittest import mock

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from story.management.commands import fetch_tumblr_stories
from story.models import Story


@mock.patch("story.management.commands.fetch_tumblr_stories.urlretrieve")
def test_fetch_tumblr_stories_download_image(p_urlretrieve):
    with mock.patch(
        "story.management.commands.fetch_tumblr_stories.open",
        mock.mock_open(read_data=""),
    ):
        image_name, image_file = fetch_tumblr_stories.download_image("tumblr.com/image.jpg")
    p_urlretrieve.assert_called_once_with("tumblr.com/image.jpg")
    assert image_name == "image.jpg"
    assert isinstance(image_file, File)


@mock.patch("story.management.commands.fetch_tumblr_stories.request_latest_stories")
@mock.patch("story.management.commands.fetch_tumblr_stories.download_image")
def test_fetch_tumblr_stories_command_existing_stories(p_download_image, p_request_latest_stories, remote_story):
    Story.objects.create(
        post_url=remote_story.url,
        name=remote_story.title,
        content=remote_story.content,
        is_story=remote_story.is_story,
    )
    p_request_latest_stories.return_value = [remote_story]
    temp_file = SimpleUploadedFile("image.jpg", "")
    p_download_image.return_value = (temp_file.name, temp_file)
    command = fetch_tumblr_stories.Command()
    command.handle()
    assert Story.objects.count() == 1


@mock.patch("story.management.commands.fetch_tumblr_stories.request_latest_stories")
@mock.patch("story.management.commands.fetch_tumblr_stories.download_image")
def test_fetch_tumblr_stories_command_new_stories(p_download_image, p_request_latest_stories, remote_story):
    Story.objects.create(
        post_url="tumblr.com/stories/99999",
        name=remote_story.title,
        content=remote_story.content,
        is_story=remote_story.is_story,
    )
    p_request_latest_stories.return_value = [remote_story]
    temp_file = SimpleUploadedFile("image.jpg", "")
    p_download_image.return_value = (temp_file.name, temp_file)
    command = fetch_tumblr_stories.Command()
    command.handle()
    assert Story.objects.count() == 2
