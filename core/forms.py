from django import forms
from django.contrib.auth import forms as auth_forms

from .models import User, Event


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

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
    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
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


class ContactForm(forms.Form):
    CHAPTER, SUPPORT = 1, 2
    CONTACT_TYPE_CHOICES = (
        (CHAPTER, 'Djangogirls Chapter'),
        (SUPPORT, 'Djangogirls Support team'),
    )

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    contact_type = forms.ChoiceField(
        choices=CONTACT_TYPE_CHOICES, widget=forms.RadioSelect
    )
    event = forms.ModelChoiceField(
        required=False,
        queryset=Event.objects.all().exclude(email__isnull=True).exclude(email__exact='')
    )
    message = forms.CharField(required=True, widget=forms.Textarea)

    def clean_event(self):
        contact_type = self.cleaned_data['contact_type']
        event = self.cleaned_data.get('event')
        if contact_type == str(self.CHAPTER):
            if not event:
                raise forms.ValidationError('Please select the event')
        return event
