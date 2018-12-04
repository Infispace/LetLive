from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views import generic

from ..models.articleModel import Article
from ..forms.articleForm import ArticleForm

class ArticleView(generic.TemplateView):
    template_name = 'home/article.html'
    form = None
    article_to_edit = None
    article_list = None

    def get(self, request, article_id=0, page='article'):
        if page is 'article_new':
            self.form = ArticleForm()
        elif page is 'article_edit':
            article_to_edit =  get_object_or_404(Article, pk=article_id)
            self.form = ArticleForm(instance=article_to_edit)
        else:
            if article_id > 0:
                self.article_to_edit =  get_object_or_404(Article, pk=article_id)
            else:
                # render some articles in my blog
                self.article_list = Article.objects.all()

        return render(request, self.template_name, {
            'page': page,
            'form': self.form,
            'article': self.article_to_edit,
            'blog_article_list': self.article_list
        })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass
