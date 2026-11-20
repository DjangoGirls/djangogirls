import pytest
from django.core.exceptions import ValidationError

from coach.models import Coach, static


def test_default_photo():
    assert Coach.objects.count() == 0
    coach = Coach.objects.create(name="Test Test", twitter_handle="@test")
    assert Coach.objects.count() == 1
    # note: always ensure that the path reflects the default_coach_photo variable in coach/models.py photo_url()
    assert coach.photo_url == static("img/global/coach-empty.png")


def test_name_twitter_handle_unique_together():
    assert Coach.objects.count() == 0
    Coach.objects.create(name="Test Coach", twitter_handle="@testcoach")
    assert Coach.objects.count() == 1
    with pytest.raises(ValidationError):
        Coach.objects.create(name="Test Coach", twitter_handle="@testcoach")
        assert Coach.objects.count() == 1
