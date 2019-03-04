from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Article
from ..forms import ArticleForm, ArticleConfirmForm

class ArticleView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        'home.add_article',
        'home.view_article',
        'home.change_article',
        'home.delete_article'
    )
    template_name = 'home/article.html'
    article = None
    article_form = None
    published_articles = None
    pending_articles = None

    def new_article(self, user):
        if(not user.has_perm('home.add_article')):
            raise PermissionDenied

    def edit_article(self, user):
        if(not user.has_perm('home.change_article')):
            raise PermissionDenied

    def delete_article(self, user):
        if(not user.has_perm('home.delete_article')):
            raise PermissionDenied

    def publish_article(self, user):
        if(not user.has_perm('home.publish_article')):
            raise PermissionDenied

    def get(self, request, article_id=0, page='article', filter='all'):
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)

        if page is 'article_new':
            self.article_form = ArticleForm()
        elif page is 'article_edit':
            self.article_form = ArticleForm(instance=self.article)
        elif page is 'article_delete' or page is 'article_publish':
            self.article_form = ArticleConfirmForm(instance=self.article)
        else:
            if filter == 'published' or filter == 'all':
                self.published_articles = Article.objects.published_articles_list(
                    status=True
                ).filter(author=request.user)
            if filter == 'pending' or filter == 'all':
                self.pending_articles = Article.objects.published_articles_list(
                    status=False
                ).filter(author=request.user)

        return render(request, self.template_name, {
            'page': page,
            'form': self.article_form,
            'article': self.article,
            'blog_published': self.published_articles,
            'blog_pending': self.pending_articles,
            'blog_filter': filter,
        })

    def post(self, request, article_id=0, page='article'):
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)

        if page is 'article_new':
            self.article_form = ArticleForm(request.POST)
            if self.article_form.is_valid():
                new_article = self.article_form.save(commit=False)
                new_article.author = request.user
                new_article.save()
                self.article_form.save_m2m()
                return HttpResponseRedirect(reverse('home:article_default'))
        elif page is 'article_edit':
            self.article_form = ArticleForm(request.POST, instance=self.article)
            if self.article_form.is_valid():
                self.article_form.save()
                return HttpResponseRedirect(reverse('home:article_default'))
        elif page is 'article_delete':
            self.article =  get_object_or_404(Article, pk=article_id)
            self.article_form = ArticleConfirmForm(request.POST, instance=self.article)
            if self.article_form.is_valid():
                self.article.delete()
                return HttpResponseRedirect(reverse('home:article_default'))
        elif page is 'article_publish':
            self.article =  get_object_or_404(Article, pk=article_id)
            self.article_form = ArticleConfirmForm(request.POST, instance=self.article)
            if self.article_form.is_valid():
                self.article.draft = False
                self.article.save()
                return HttpResponseRedirect(reverse('home:article_default'))

        return render(request, self.template_name, {
            'page': page,
            'form': self.article_form,
            'article': self.article,
        })
