from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from captcha.fields import ReCaptchaField

from .models import User, ContactEmail, Event


class BetterReCaptchaField(ReCaptchaField):
    """A ReCaptchaField that always works in DEBUG mode"""
    def clean(self, values):
        if settings.DEBUG:
            return values[0]
        return super(BetterReCaptchaField, self).clean(values)


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
