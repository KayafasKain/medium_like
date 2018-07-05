from django import forms
from django.apps import apps
from django.contrib.auth import (
    get_user_model,
    authenticate,
)

User = get_user_model()
Profile = apps.get_model('profile_app', 'Profile')


class ProfileEditForm(forms.ModelForm):

    def __init__ (self, *args, **kwargs):
        profile = kwargs.pop('profile')
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = profile.phone_number
        self.fields['about'].initial = profile.about


    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'about',
        ]

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['new_password', 'password']
        error_messages = {
            'password': {
                'not_match': 'password not match',
            },
        }

    def clean(self):
        password = self.cleaned_data.get("password")
        if password:
            user_verify = authenticate(username=User.username, password=password)
            if not user_verify:
                raise forms.ValidationError({
                    'password': self.Meta.error_messages['password']['not_match']
                })
