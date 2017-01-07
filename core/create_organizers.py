from .models import User


def add_organizer(organizer, event):
    """
        Add organizer to the event.

        TODO: we need to think if create_organizers and create_events
        are the best place for these logic. Maybe we should move it back to
        the models.
    """
    defaults = {
        "first_name": organizer.first_name,
        "last_name": organizer.last_name,
        "is_staff": True,
        "is_active": True
    }
    user, created = User.objects.get_or_create(
        email=organizer.email,
        defaults=defaults
    )
    if created:
        password = user.generate_password()
        user.add_to_organizers_group()

    event.invite_organizer_to_team(user, created, password)
    return user


def create_organizers(event, event_application, email_password):
    """ Create or get User objects based on EventApplication's Coorganizers
    """
    organizers = []
    for organizer in event_application.coorganizers.all():
        user = add_organizer(organizer, event)
        organizers.append(user)

    return organizers
