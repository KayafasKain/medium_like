from django import forms
from django.apps import apps

PostArticle = apps.get_model('post_app', 'PostArticle')
class CreateArticleForm(forms.ModelForm):

    class Meta:
        model = PostArticle
        fields = [
            'title',
            'description',
            'text',
            'category',
        ]

class ArticleEditForm(forms.ModelForm):

    def __init__ (self, *args, **kwargs):
        article = kwargs.pop('article')
        super(ArticleEditForm, self).__init__(*args, **kwargs)
        self.fields['title'].initial = article.title
        self.fields['description'].initial = article.description
        self.fields['text'].initial = article.text
        self.fields['category'].initial = article.category

    class Meta:
        model = PostArticle
        fields = [
            'title',
            'description',
            'text',
            'category',
        ]