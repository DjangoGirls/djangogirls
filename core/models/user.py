from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Group
from django.db import models

from core.models.managers.user import UserManager
from core.slack_client import invite_user_to_slack


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"

    def invite_to_slack(self):
        invite_user_to_slack(self.email, self.first_name)

    def generate_password(self):
        password = User.objects.make_random_password()
        self.set_password(password)
        self.save()
        return password

    def add_to_organizers_group(self):
        try:
            group = Group.objects.get(name="Organizers")
        except Group.DoesNotExist:
            return

        self.groups.add(group)

    def __str__(self):
        if not self.first_name and not self.last_name:
            return f"{self.email}"
        return f"{self.get_full_name()} ({self.email})"

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
