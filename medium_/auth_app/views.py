from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from .forms import UserRegisterForm, UserLoginForm, ProfileRegisterForm
from django.apps import apps


Profile = apps.get_model('profile_app', 'Profile')

User = get_user_model()

class LoginView(FormView):
    template_name = 'auth_app/login.html'
    form_class = UserLoginForm
    context_object_name = 'login'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate( self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('create-loan'))
        redirect('/')

login_view = LoginView.as_view()

class MyLogoutView(RedirectView):
    context_object_name = 'logout'
    success_url = '/'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return self.success_url

logout_view = MyLogoutView.as_view()


class RegisterView(FormView):
    template_name = 'auth_app/register.html'
    form_class = UserRegisterForm
    context_name = 'register'
    model = User

    def form_valid(self, form):
        try:
            user = self.model.objects.get(email=form.cleaned_data['email'])
        except self.model.DoesNotExist as e:
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()

        return HttpResponseRedirect(reverse('register-profile', kwargs={'pk': str(user.pk)}))

register = RegisterView.as_view()

class CreateProfileView(FormView): #Work In Progress
    template_name = 'auth_app/register_profile.html'
    form_class = ProfileRegisterForm
    context_name = 'register-profile'
    model = Profile
    user_model = User

    def form_valid(self, form):
        try:
            profile = self.model.objects.get(user=self.kwargs['pk'])
        except self.model.DoesNotExist as e:
            profile = form.save()
        profile.user = self.user_model.objects.get(pk=self.kwargs['pk'])
        profile.save()
        return redirect('/')

create_profile = CreateProfileView.as_view()