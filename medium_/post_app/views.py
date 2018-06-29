from django.shortcuts import render
from django.apps import apps
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

PostArticle = apps.get_model('post_app', 'PostArticle')

Post = apps.get_model('post_app', 'Status')
class ArticleList(ListView):
    model = PostArticle
    template_name = 'post_app/loan_list.html'
    context_object_name = 'article-list'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all()

article_post_list = ArticleList.as_view()

class OwnArticleList(ListView):
    model = PostArticle
    template_name = 'post_app/loan_list.html'
    context_object_name = 'own-article-list'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

own_article_post_list = OwnArticleList.as_view()

class ShowArticle(DetailView):
    model = PostArticle
    template_name = 'post_app/article.html'
    context_object_name = 'show-article'

    def get_queryset(self):
        return self.model.objects.get(pk=self.kwargs['pk'])