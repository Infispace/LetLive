from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.urls import reverse
from django.utils import timezone

from home.models import Article
from home.forms import ArticleConfirmForm

class PublishView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        'home.publish_article',
        'home.change_article',
        'home.delete_article'
    )
    template_name = 'home/article_publish.html'
    article = None
    publish_form = None
    publish_article_list = []

    def get(self, request, article_id=0, page=''):
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)
        else:
            self.publish_article_list = Article.objects.published_articles_list(
                status=False
            ).exclude(
                author=request.user
            ).filter(
                draft=False
            )

        if page == '':
            self.publish_form = ArticleConfirmForm(instance=self.article)

        return render(request, self.template_name, {
            'page': page,
            'form': self.publish_form,
            'article': self.article,
            'article_list': self.publish_article_list,
        })

    def post(self, request, article_id=0, page=''):
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)
            self.article_form = ArticleConfirmForm(request.POST, instance=self.article)
            if self.article_form.is_valid():
                self.article.publisher = request.user.publisher
                self.article.publish_date_time = timezone.now()
                self.article.save()
                return HttpResponseRedirect(reverse('home:publish_article'))

        return render(request, self.template_name, {
            'page': page,
            'form': self.publish_form,
            'article': self.article,
        })
