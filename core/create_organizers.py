from .models import User


def create_organizers(event, event_application, email_password):
    """
        Create or get User objects based on EventApplication's
    """
    organizers = []
    for organizer in event_application.coorganizers.all():
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
        organizers.append(user)

    return organizers
