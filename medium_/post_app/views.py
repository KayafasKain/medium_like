from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.apps import apps
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from .forms import CreateArticleForm, ArticleEditForm

PostArticle = apps.get_model('post_app', 'PostArticle')
Status = apps.get_model('post_app', 'Status')

class ArticleList(ListView):
    model = PostArticle
    template_name = 'post_app/post_list.html'
    context_object_name = 'article-list'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.all()

article_post_list = ArticleList.as_view()

class OwnArticleList(ListView):
    model = PostArticle
    template_name = 'post_app/post_list.html'
    context_object_name = 'own-article-list'
    paginate_by = 10

    def get_queryset(self):
        return PostArticle.objects.filter(user=self.request.user)

own_article_post_list = OwnArticleList.as_view()

class ShowArticle(DetailView):
    model = PostArticle
    template_name = 'post_app/article.html'
    context_object_name = 'show-article'

show_single_article = ShowArticle.as_view()

class CreateArticleView(FormView):
    template_name = 'post_app/article_create.html'
    form_class = CreateArticleForm
    context_name = 'article-create'
    model = PostArticle
    success_url = '/'

    def form_valid(self, form):
        article = form.save()
        article.status = Status.objects.get(name='Review')
        article.user = self.request.user
        article.save()
        return redirect(reverse('own-article-list'))


create_article = CreateArticleView.as_view()

class EditArticle(FormView):
    template_name = 'post_app/article_create.html'
    form_class = ArticleEditForm
    context_name = 'article-edit'
    model = PostArticle

    def get_form_kwargs(self):
        kwargs = super(EditArticle, self).get_form_kwargs()
        self.current_article = self.model.objects.get(pk=self.kwargs['pk'])
        kwargs.update({
            'article': self.current_article
        })
        return kwargs

    def form_valid(self, form):
        article = self.current_article
        article.title = form.cleaned_data['title']
        article.description = form.cleaned_data['description']
        article.text = form.cleaned_data['text']
        article.category = form.cleaned_data['category']
        article.status = Status.objects.get(name='Review')
        article.save()
        return redirect(reverse('own-article-list'))

edit_article = EditArticle.as_view()