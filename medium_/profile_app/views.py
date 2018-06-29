from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.apps import apps
from .forms import ProfileEditForm
from .utils.classifiers.numerical_classifier import NumericalClassifier as NC

Profile = apps.get_model('profile_app', 'Profile')

class EditProfileView(FormView): #Work In Progress
    template_name = 'auth_app/register_profile.html'
    form_class = ProfileEditForm
    context_name = 'edit-profile'
    model = Profile
    class_model = ClientClass

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        self.current_profile = Profile.objects.get(user=self.request.user)
        kwargs.update({
            'profile': self.current_profile
        })
        return kwargs

    def form_valid(self, form):
        profile = self.current_profile
        profile.income_yearly = form.cleaned_data['income_yearly']
        profile.employer_name = form.cleaned_data['employer_name']
        profile.birth_date = form.cleaned_data['birth_date']
        profile.employment_type = form.cleaned_data['employment_type']
        clas = NC(profile)
        profile.client_class = clas.get_user_class()
        profile.save()
        return redirect('/')

edit_profile = EditProfileView.as_view()