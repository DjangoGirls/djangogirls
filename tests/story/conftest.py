import pytest

from story.models import Story


@pytest.fixture
def data_dict():
    """
    name = models.CharField(max_length=200)
    content = models.TextField(null=True)
    post_url = models.URLField()
    image = models.ImageField(upload_to="stories/", null=True)
    created = models.DateField(auto_now_add=True)
    # False means a regular blogpost, not a story
    is_story = models.BooleanField(default=True)
    """

    return {
        'name': 'Story 1',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                   'labore et dolore magna aliqua. Ut pharetra sit amet aliquam id diam maecenas ultricies mi.',
        'is_story': True,
        'post_url': 'story-1-url',
    }


@pytest.fixture
def blog_posts(db):
    return Story.objects.bulk_create(
        [
            Story(name='Post 1', content='Lorem ipsum dolor sit amet', is_story=False, post_url='post-1-url'),
            Story(name='Post 2', content='Lorem ipsum dolor sit amet', is_story=False, post_url='post-2-url'),
            Story(name='Post 3', content='Lorem ipsum dolor sit amet', is_story=False, post_url='post-3-url'),
            Story(name='Post 4', content='Lorem ipsum dolor sit amet', is_story=False, post_url='post-4-url'),
            Story(name='Post 5', content='Lorem ipsum dolor sit amet', is_story=False, post_url='post-5-url')
        ]
    )
