from io import StringIO
from unittest import mock

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command

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


@mock.patch("requests.get")
def test_fetch_stories_if_feed_not_found(mock_get):
    mock_response = mock.MagicMock()
    mock_response.status_code = 404
    mock_response.content = "<xml></xml>"
    mock_response.ok = False
    mock_response.reason = "Not Found"
    mock_get.return_value = mock_response

    with StringIO() as out:
        call_command("fetch_stories", stdout=out)
        assert "Not Found" in out.getvalue()


@mock.patch("requests.get")
def test_fetch_stories_a_blog_post(mock_get):
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.content = """<rss version="2.0">
<channel>
<description/>
<title>Django Girls Blog</title>
<generator>Tumblr (3.0; @djangogirls)</generator>
<link>https://blog.djangogirls.org/</link>
<item>
<title>Blog title</title>
<description>Post description</description>
<link>https://blog.djangogirls.org/post/791047576209227776</link>
<guid>https://blog.djangogirls.org/post/791047576209227776</guid>
<pubDate>Tue, 05 Aug 2025 14:49:16 +0100</pubDate>
<category>codewithkindness</category>
</item>
</channel>
</rss>"""
    mock_get.return_value = mock_response

    with StringIO() as out:
        call_command("fetch_stories", stdout=out)

    stories = Story.objects.all()
    assert stories.count() == 1
    story = stories.first()
    assert story.name == "Blog title"
    assert story.is_story is False


@mock.patch("requests.get")
def test_fetch_stories_a_story(mock_get):
    """A blog post is considered a story (Story.is_story) if its
    title starts with 'Your Django Story: Meet'."""
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.content = """<rss version="2.0">
<channel>
<description/>
<title>Django Girls Blog</title>
<generator>Tumblr (3.0; @djangogirls)</generator>
<link>https://blog.djangogirls.org/</link>
<item>
<title>Your Django Story: Meet Pony</title>
<description>Post description</description>
<link>https://blog.djangogirls.org/post/791047576209227776</link>
<guid>https://blog.djangogirls.org/post/791047576209227776</guid>
<pubDate>Tue, 05 Aug 2025 14:49:16 +0100</pubDate>
<category>codewithkindness</category>
</item>
</channel>
</rss>"""
    mock_get.return_value = mock_response

    with StringIO() as out:
        call_command("fetch_stories", stdout=out)

    stories = Story.objects.all()
    assert stories.count() == 1
    story = stories.first()
    assert story.name == "Pony"
    assert story.is_story is True
