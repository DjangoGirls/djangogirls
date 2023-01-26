from coach.models import DEFAULT_COACH_PHOTO, Coach


def test_default_photo():
    assert Coach.objects.count() == 0
    coach = Coach.objects.create(name="Test Test", twitter_handle="@test")
    assert Coach.objects.count() == 1
    assert coach.photo_url == DEFAULT_COACH_PHOTO
