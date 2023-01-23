import pytest


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
        "name": "Story 1",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
        "labore et dolore magna aliqua. Ut pharetra sit amet aliquam id diam maecenas ultricies mi.",
        "is_story": True,
        "post_url": "story-1-url",
    }
