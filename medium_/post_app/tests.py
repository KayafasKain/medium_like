from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
)
from django.test import TestCase
from django.test import Client
from django.apps import apps

User = get_user_model()
PostArticle = apps.get_model('post_app', 'PostArticle')
Category = apps.get_model('post_app', 'Category')
Status = apps.get_model('post_app', 'Status')

class ArticleTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser2',
            'password': 'secret',
            'email': 'email@email.com'
        }

        self.article = {
            'title': 'test322',
            'description': 'description',
            'text': 'text322',
            'category': 1
        }
        Category.objects.create(name='test_topic')
        Status.objects.create(name='Review')
        user = User.objects.create_user(**self.credentials)
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])


    def test_create_article_positive(self):
        response = self.client.post('/create_article/', self.article, follow=True)
        self.assertGreater(
            len(PostArticle.objects.all()),
            0
        )

    def test_create_article_negative(self):
        negative_article =  self.article
        negative_article['category'] = "lol322"

        response = self.client.post('/create_article/', negative_article, follow=True)
        self.assertEqual(
            len(PostArticle.objects.filter(title=self.article['title'])),
            0
        )

    def test_get_article_list(self):
        self.client.post('/create_article/', self.article, follow=True)
        response = self.client.get('', follow=True)
        response.context['object_list']
        self.assertGreater(
            len(response.context['object_list']),
            0
        )

    def test_get_article_list_own(self):
        self.client.post('/create_article/', self.article, follow=True)
        response = self.client.get('/own_article_list/', follow=True)
        response.context['object_list']
        self.assertGreater(
            len(response.context['object_list']),
            0
        )

    def test_get_article_detail(self):
        self.client.post('/create_article/', self.article, follow=True)
        response = self.client.get('/show_article/1', follow=True)
        self.assertIsNotNone(
            response.context['object']
        )

    def test_edit_article(self):
        self.client.post('/create_article/', self.article, follow=True)
        edit_article =  self.article
        edit_article['title'] = "228"
        response = self.client.post('/edit_article/1', edit_article, follow=True)
        self.assertGreater(
            len(PostArticle.objects.filter(title=edit_article['title'])),
            0
        )