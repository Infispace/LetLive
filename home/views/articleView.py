from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Article, Topic
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
    _article = None                     #unsaved article
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

        try:
            self._article = Article()
            self._article.title = request.session['_article']['title']
            self._article.content = request.session['_article']['content']
            self._article.topic = get_object_or_404(
                Topic,
                pk=int(request.session['_article']['topic'])
            )
            if page is 'article_new':
                del request.session['_article']
        except Exception as e:
            pass 
          
        # Filter with page
        if page is 'article_new':
            edit_article = False
            try :
                referer = request.META['HTTP_REFERER']
                url = request.build_absolute_uri(reverse('home:article_new_view'))
                if referer == url:
                    edit_article = True
            except Exception as e:
                pass 
                            
            if self._article is not None and edit_article:
                self.article_form = ArticleForm(instance=self._article)
            else:
                self.article_form = ArticleForm()
            
        elif page is 'article_new_view':
            self.article_form = ArticleForm(instance=self._article)   
                 
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
            'article_': self._article,
            'blog_published': self.published_articles,
            'blog_pending': self.pending_articles,
            'blog_filter': filter,
        })

    def post(self, request, article_id=0, page='article'):
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)

        # Filter with page
        if page is 'article_new':
            self.article_form = ArticleForm(request.POST)
            if self.article_form.is_valid():
                new_article = self.article_form.save(commit=False)
                new_article.author = request.user
                new_article.save()
                self.article_form.save_m2m()
                return HttpResponseRedirect(reverse('home:article_default'))
                
        elif page is 'article_new_view':
            self.article_form = ArticleForm(request.POST)
            self._article = self.article_form.save(commit=False)
            request.session['_article'] = {
                'title': self._article.title,
                'topic': str(self._article.topic.id),
                'content': self._article.content,
            }
            return HttpResponseRedirect(reverse('home:article_new_view'))
                        
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
            'article_': self._article,
        })
        
