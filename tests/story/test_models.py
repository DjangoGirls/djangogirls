from story.models import Story


def test_story_creation(data_dict):

    story = Story.objects.create(**data_dict)
    assert str(story) == data_dict["name"]
