from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template.loader import render_to_string
from slacker import Error as SlackerError

from core.models import ContactEmail, Event, User
from core.slack_client import user_invite


class BetterReCaptchaField(ReCaptchaField):
    """A ReCaptchaField that always works in DEBUG mode"""
    def clean(self, values):
        if settings.DEBUG:
            return values[0]
        return super(BetterReCaptchaField, self).clean(values)


class AddOrganizerForm(forms.Form):
    """
    Custom form for adding new organizers to an existing event.

    If user of given email already exists, they're added to the event and
    receive e-mail notification about it.

    If user is new, they're created (randomly generated password), invited
    to Slack and receive e-mail notification with instructions to login
    (including password).
    """
    event = forms.ModelChoiceField(queryset=Event.objects.all())
    name = forms.CharField(label="Organizer's first and last name")
    email = forms.CharField(label="E-mail address", validators=[validate_email])

    def __init__(self, event_choices=None, *args, **kwargs):
        super(AddOrganizerForm, self).__init__(*args, **kwargs)
        if event_choices:
            self.fields['event'].queryset = event_choices

    def invite_to_slack(self, email, name):
        try:
            user_invite(email, name)
        except (ConnectionError, SlackerError) as e:
            self._errors.append('Slack invite unsuccessful, reason: {}'.format(e))

    def notify_existing_user(self, user):
        content = render_to_string('emails/existing_user.html', {
            'user': user,
            'event': self.cleaned_data['event']
        })
        subject = 'You have been granted access to new Django Girls event'
        self.send_email(content, subject, user)

    def notify_new_user(self, user):
        content = render_to_string('emails/new_user.html', {
            'user': user,
            'event': self.cleaned_data['event'],
            'password': self._password,
            'errors': self._errors,
        })
        subject = 'Access to Django Girls website'
        self.send_email(content, subject, user)

    def send_email(self, content, subject, user):
        send_mail(subject, content, "Django Girls <hello@djangogirls.org>",
                  [user.email])

    def save(self, *args, **kwargs):
        assert self.is_valid()
        self._errors = []
        email = self.cleaned_data['email']
        event = self.cleaned_data['event']

        user, created = User.objects.get_or_create(email=email)
        event.team.add(user)
        if created:
            self._password = User.objects.make_random_password()
            user.first_name = self.cleaned_data['name'].split(' ')[0]
            user.last_name = self.cleaned_data['name'].replace(user.first_name, '')
            user.is_staff = True
            user.is_active = True
            user.set_password(self._password)
            user.save()
            user.groups.add(1)
            self.invite_to_slack(email, user.first_name)
            self.notify_new_user(user)
        else:
            self.notify_existing_user(user)
        return user


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class UserLimitedChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class EventChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}, {}".format(obj.city, obj.country)


class ContactForm(forms.ModelForm):
    event = EventChoiceField(
        queryset=Event.objects.public().distinct('city', 'country').order_by('city'),
        required=False, label="Django Girls workshop in..."
    )
    captcha = BetterReCaptchaField()

    class Meta:
        model = ContactEmail
        fields = (
            'name',
            'email',
            'contact_type',
            'event',
            'message',
        )
        widgets = {'contact_type': forms.RadioSelect}

    def clean_event(self):
        contact_type = self.cleaned_data.get('contact_type')
        event = self.cleaned_data.get('event')
        if contact_type == ContactEmail.CHAPTER:
            if not event:
                raise forms.ValidationError('Please select the event')
        return event
