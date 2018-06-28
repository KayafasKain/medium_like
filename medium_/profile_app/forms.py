from django import forms
from django.apps import apps

Profile = apps.get_model('profile_app', 'Profile')

BIRTH_YEAR_CHOICES = ( i for i in range(1900, 2000) )

class ProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))

    def __init__ (self, *args, **kwargs):
        profile = kwargs.pop('profile')
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['income_yearly'].initial = profile.income_yearly
        self.fields['employer_name'].initial = profile.employer_name
        self.fields['birth_date'].initial = profile.birth_date
        self.fields['employment_type'].initial = profile.employment_type


    class Meta:
        model = Profile
        fields = [
            'income_yearly',
            'employer_name',
            'birth_date',
            'employment_type',
        ]
