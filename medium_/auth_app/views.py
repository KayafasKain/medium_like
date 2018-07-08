from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

import json

import telepot
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import RedirectView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, UserLoginForm, ProfileRegisterForm, VerifyForm
from django.apps import apps
from django.http import JsonResponse
from telepot.loop import MessageLoop
import re
import string
import random




Profile = apps.get_model('profile_app', 'Profile')
Telegramm = apps.get_model('profile_app', 'Telegramm')

User = get_user_model()

TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def handle(request):
    chat_id = request['chat']['id']
    cmd = request.get('text')
    phones = re.findall(r'^\+380\d{3}\d{2}\d{2}\d{2}$', cmd)

    try:
         profile = Profile.objects.get(phone_number=phones[0])
    except:
        TelegramBot.sendMessage(chat_id, 'Invalid phone number!')

    if profile:
        telegramm = Telegramm()
        telegramm.user = profile.user
        telegramm.tele_id = chat_id
        telegramm.save()
        TelegramBot.sendMessage(chat_id, 'Got it, Sir!')

    return JsonResponse({}, status=200)

MessageLoop(TelegramBot, handle).run_as_thread()


class LoginView(FormView):
    template_name = 'auth_app/login.html'
    form_class = UserLoginForm
    context_object_name = 'login'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate( self.request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                return HttpResponseRedirect(reverse('verify-code', kwargs={'pk': str(user.pk)}))
            login(self.request, user)
            return HttpResponseRedirect(reverse('article-list'))
        redirect('/')

login_view = LoginView.as_view()

class VerifyView(FormView):
    template_name = 'auth_app/verify_code.html'
    form_class = VerifyForm
    context_object_name = 'verify-code'

    def get_form_kwargs(self):
        kwargs = super(VerifyView, self).get_form_kwargs()

        if  not self.request.POST:
            self.user = User.objects.get(pk=self.kwargs['pk'])
            self.current_code = code_generator()
            telegramm_var = Telegramm.objects.get(user_id=self.user.pk)
            telegramm_var.code = self.current_code
            telegramm_var.save()
            TelegramBot.sendMessage(telegramm_var.tele_id, self.current_code)
        else:
            self.user = User.objects.get(pk=self.kwargs['pk'])
            telegramm_var = Telegramm.objects.get(user_id=self.user.pk)
            self.current_code = telegramm_var.code
        return kwargs

    def form_valid(self, form):
        if form.cleaned_data['code'] == self.current_code:
            login(self.request, self.user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('article-list'))
        return HttpResponseRedirect(reverse('login'))

verify_view = VerifyView.as_view()

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

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate( self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

        return HttpResponseRedirect(reverse('register-profile', kwargs={'pk': str(user.pk)}))

register = RegisterView.as_view()

class CreateProfileView(FormView):
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