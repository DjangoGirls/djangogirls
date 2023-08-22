import pytest
from django.core.exceptions import ValidationError

from coach.models import DEFAULT_COACH_PHOTO, Coach


def test_default_photo():
    assert Coach.objects.count() == 0
    coach = Coach.objects.create(name="Test Test", twitter_handle="@test")
    assert Coach.objects.count() == 1
    assert coach.photo_url == DEFAULT_COACH_PHOTO


def test_name_twitter_handle_unique_together():
    assert Coach.objects.count() == 0
    Coach.objects.create(name="Test Coach", twitter_handle="@testcoach")
    assert Coach.objects.count() == 1
    with pytest.raises(ValidationError):
        Coach.objects.create(name="Test Coach", twitter_handle="@testcoach")
        assert Coach.objects.count() == 1
