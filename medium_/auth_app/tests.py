from django.contrib.auth.models import User
from django.test import TestCase
from django.apps import apps
Profile = apps.get_model('profile_app', 'Profile')

class LogInTest(TestCase):
    def setUp(self):
        self.credentials_positive = {
            'username': 'testuser',
            'password': 'secret'}
        self.credentials_negative = {
            'username': 'testuser228',
            'password': 'secret322'}

        User.objects.create_user(**self.credentials_positive)

    def test_login_positive(self):
        response = self.client.post('/login/', self.credentials_positive, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_login_negative(self):
        response = self.client.post('/login/', self.credentials_negative, follow=True)
        self.assertFalse(response.context['user'].is_active)

class RegisterTest(TestCase):
    def setUp(self):
        self.credentials_positive = {
            'username': 'testuser',
            'email':'email@email.com',
            'password': 'secret'}
        self.credentials_negative = {
            'username': 'testuser',
            'email':'emailemail.cm',
            'password': 'secret'}

    def test_register_positive(self):
        response = self.client.post('/register/', self.credentials_positive, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_register_negative(self):
        response = self.client.post('/register/', self.credentials_negative, follow=True)
        self.assertFalse(response.context['user'].is_active)


class ProfileTest(TestCase):
    def setUp(self):
        self.credentials_positive = {
            'phone_number': '+380991257600',
            'about':'email@email.com',}

        self.credentials_negative = {
            'phone_number': '+380993321253600',
            'about':'email@email.com',}

        self.credentials_user = {
            'username': 'testuser',
            'email':'email@email.cm',
            'password': 'secret'}

        User.objects.create_user(**self.credentials_user)
        self.user_pk = User.objects.get(username=self.credentials_user['username']).pk

    def test_register_positive(self):
        response = self.client.post('/create_profile/' + str(self.user_pk), self.credentials_positive, follow=True)
        self.assertEqual(
            len(Profile.objects.filter(phone_number=self.credentials_positive['phone_number'])),
            1
        )

    def test_register_negative(self):
        response = self.client.post('/create_profile/' + str(self.user_pk), self.credentials_negative, follow=True)
        self.assertEqual(
            len(Profile.objects.filter(phone_number=self.credentials_positive['phone_number'])),
            0
        )