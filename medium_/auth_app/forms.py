from django import forms
from django.apps import apps
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()
Profile = apps.get_model('profile_app', 'Profile')

class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']
        labels = {'Login'}
        help_texts = {'enter login and password, then press submit button'}
        error_messages = {
            'username': {
                'required': 'please, don`t leave field blank',
                'not_found': 'please, provide us with valid username',
                'inactive': 'current user is no longer active'
            },
            'password': {
                'not_match': 'wrong username or password',
            },
        }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError({
                    'username': self.Meta.error_messages['username']['not_found']
                })
            if not user.check_password(password):
                raise forms.ValidationError({
                    'password': self.Meta.error_messages['password']['not_match']
                })
            if not user.is_active:
                raise forms.ValidationError({
                    'username': self.Meta.error_messages['username']['inactive']
                })


class ProfileRegisterForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'about',
        ]

class VerifyForm(forms.Form):
    code = forms.CharField()

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]
        error_messages = {
            'email': {
                'taken': 'his email has already been registered',
            },
        }

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError({
                'email': self.Meta.error_messages['email']['taken']
            })

        return super(UserRegisterForm,self).clean(*args, **kwargs)

