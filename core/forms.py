import random
import string

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from captcha.fields import ReCaptchaField
from slacker import Slacker
from slacker import Error as SlackerError

from .models import User, ContactEmail, Event


slack = Slacker(settings.SLACK_API_KEY)


class BetterReCaptchaField(ReCaptchaField):
    """A ReCaptchaField that always works in DEBUG mode"""
    def clean(self, values):
        if settings.DEBUG:
            return values[0]
        return super(BetterReCaptchaField, self).clean(values)


class AddOrganizerForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all())
    name = forms.CharField(label="Organizer's full name")
    email = forms.CharField(label="E-mail address")

    def __init__(self, event_choices, *args, **kwargs):
        super(AddOrganizerForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = event_choices

    def generate_password(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    def invite_to_slack(self, email, name):
        try:
            response = slack.users.invite(email, name)
        except (ConnectionError, SlackerError) as e:
            self._errors.append('Slack invite unsuccessful, reason: {}'.format(e))

    def notify_existing_user(self, user):
        content = render_to_string('emails/existing_user.html', {
            'user': user,
            'event': self.cleaned_data['event']
        })
        subject = 'You have been granted to new Django Girls event'
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
            [user.email], fail_silently=True)

    def save(self, *args, **kwargs):
        self._errors = []
        email = self.cleaned_data['email']
        event = self.cleaned_data['event']
        if not User.objects.filter(email=email).exists():
            self._password = self.generate_password()
            first_name = self.cleaned_data['name'].split(' ')[0]
            last_name = self.cleaned_data['name'].replace(first_name, '')
            user = User.objects.create(email=email,
                                        first_name=first_name,
                                        last_name=last_name,
                                        is_active=True,
                                        is_staff=True)
            user.set_password(self._password)
            user.save()
            user.groups.add(1)
            event.team.add(user)
            event.save()
            self.invite_to_slack(email, first_name)
            self.notify_new_user(user)
        else:
            user = User.objects.get(email=email)
            event.team.add(user)
            event.save()
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
