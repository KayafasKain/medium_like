from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.apps import apps
from .forms import ProfileEditForm, ChangePasswordForm
from django.http import HttpResponseRedirect

Profile = apps.get_model('profile_app', 'Profile')
User = get_user_model()

class EditProfileView(FormView): #Work In Progress
    template_name = 'profile_app/edit_profile.html'
    form_class = ProfileEditForm
    context_name = 'edit-profile'
    model = Profile

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        self.current_profile = Profile.objects.get(user=self.request.user)
        kwargs.update({
            'profile': self.current_profile
        })
        return kwargs

    def form_valid(self, form):
        profile = self.current_profile
        profile.phone_number = form.cleaned_data['phone_number']
        profile.about = form.cleaned_data['about']
        profile.save()
        return redirect('/')

edit_profile = EditProfileView.as_view()

class ChangePasswordView(FormView):
    template_name = 'profile_app/change_password.html'
    form_class = ChangePasswordForm
    context_name = 'ch-password'

    def form_valid(self, form):
        password = form.cleaned_data['password']
        user_verify = authenticate( self.request, username=self.request.user.username, password=password)
        if user_verify:
            self.request.user.set_password(form.cleaned_data['password-new'])
            self.request.user.save()

        return HttpResponseRedirect(reverse('article-list'))


change_password = ChangePasswordView.as_view()