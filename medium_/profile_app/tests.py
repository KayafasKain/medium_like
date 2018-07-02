from django.contrib.auth import (
    get_user_model,
)
from django.test import TestCase
from django.test import Client
from django.apps import apps

User = get_user_model()
Profile = apps.get_model('profile_app', 'Profile')

class ProfileTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret',
            'email': 'email@email.com'
        }

        self.credentials_profile = {
            'phone_number': '+380991257600',
            'about':'email@email.com',
        }

        user = User.objects.create_user(**self.credentials)
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])

    def test_edit_profile(self):
        self.client.post('/create_profile/1', self.credentials_profile, follow=True)
        edit_article =  self.credentials_profile
        edit_article['about'] = 'loooool'
        response = self.client.post('/edit_profile/', edit_article, follow=True)
        self.assertEqual(
            Profile.objects.get(pk=1).about,
            'loooool'
        )

    def test_change_password(self):
        self.client.post('/create_profile/1', self.credentials_profile, follow=True)
        change_password = {
            'new_password': '228322',
            'password': self.credentials['password']
        }

        response = self.client.post('/change_password/', change_password, follow=True)
        response = self.client.post('/login/', {
            'username': self.credentials['username'],
            'password': '228322' }, follow=True)
        self.assertTrue(response.context['user'].is_active)