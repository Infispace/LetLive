from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.serializers import serialize
from django.urls import reverse
from django.views.generic import TemplateView

from home.models import Article, Topic, Author, Subscriber
from home.forms import ArticleForm, ArticleConfirmForm

class ArticleView(PermissionRequiredMixin, TemplateView):
    permission_required = ('home.view_article')
    template_name = 'home/article.html'
    article = None
    _article = None   #unsaved article
    article_form = None
    published_articles = None
    pending_articles = None

    def paid_subscriber(self, user):
        paid = False;
        try:
            if Subscriber.objects.filter(user_id=user.id).exists():
                subsc = Subscriber.objects.get(user_id=user.id)                
                
                if subsc.subscription_type == Subscriber.PAID:
                    paid = True
        except Exception as e:
            pass
        
        return paid

    def new_article(self, user):
        paid = self.paid_subscriber(user)
        if(not user.has_perm('home.add_article') and not paid):
            raise PermissionDenied

    def edit_article(self, user):
        paid = self.paid_subscriber(user)
        if(not user.has_perm('home.change_article') and not paid):
            raise PermissionDenied

    def delete_article(self, user):
        paid = self.paid_subscriber(user)
        if(not user.has_perm('home.delete_article') and not paid):
            raise PermissionDenied

    def get(
        self, 
        request, 
        article_id=0, 
        page='article', 
        filter='all', 
        user_name='',
        *args, 
        **kwargs,
    ):
        super().get(self, request, *args, **kwargs)
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
            self.new_article(request.user)
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
            self.new_article(request.user)
            self.article_form = ArticleForm(instance=self._article)   
                 
        elif page is 'article_edit':
            self.edit_article(request.user)
            self.article_form = ArticleForm(instance=self.article)
            
        elif page is 'article_delete' or page is 'article_publish':
            if page is 'article_delete':
              self.delete_article(request.user)
            elif page is 'article_publish':
              self.new_article(request.user)
              self.edit_article(request.user)
              
            self.article_form = ArticleConfirmForm(instance=self.article)
            
        elif page is 'blog':
            perm = False
            auth = None
            user = get_object_or_404(User, username=user_name)            

            try:
                if Author.objects.filter(user_id=user.id).exists():
                    auth = Author.objects.get(user_id=user.id)
                    perm = True
                elif Subscriber.objects.filter(user_id=user.id).exists(): 
                    auth = Subscriber.objects.get(user_id=user.id)
                    if auth.subscription_type == Subscriber.PAID:
                        perm = True
            except ObjectDoesNotExist as e:
                pass                           
            
            if perm == False or auth== None:
                raise PermissionDenied
                
            self.published_articles = Article.objects.published_articles_list(
                status=True
            ).filter(author=auth.user)
        
        elif page is 'my_blog' or page is 'article_filter':
            try:
                sub = Subscriber.objects.get(user_id=request.user.id)
                if sub.subscription_type == Subscriber.FREE:
                    raise PermissionDenied
            except ObjectDoesNotExist as e:
                pass
             
            if filter == 'published' or filter == 'all':
                self.published_articles = Article.objects.published_articles_list(
                    status=True
                ).filter(author=request.user)
            if filter == 'pending' or filter == 'all':
                self.pending_articles = Article.objects.published_articles_list(
                    status=False
                ).filter(author=request.user)
        
        else:
            return HttpResponseNotFound()

        return render(request, self.template_name, {
            'page': page,
            'form': self.article_form,
            'article': self.article,
            'article_': self._article,
            'blog_published': self.published_articles,
            'blog_pending': self.pending_articles,
            'blog_filter': filter,
        })

    def post(self, request, article_id=0, page='article', *args, **kwargs):
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)

        # Filter with page
        if page is 'article_new':
            self.new_article(request.user)
            self.article_form = ArticleForm(request.POST)
            if self.article_form.is_valid():
                new_article = self.article_form.save(commit=False)
                new_article.author = request.user
                new_article.save()
                self.article_form.save_m2m()
                return HttpResponseRedirect(reverse('home:article_default'))
                
        elif page is 'article_new_view':
            self.new_article(request.user)
            self.article_form = ArticleForm(request.POST)
            self._article = self.article_form.save(commit=False)
            request.session['_article'] = {
                'title': self._article.title,
                'topic': str(self._article.topic.id),
                'content': self._article.content,
            }
            return HttpResponseRedirect(reverse('home:article_new_view'))
                        
        elif page is 'article_edit':
            self.edit_article(request.user)
            self.article_form = ArticleForm(request.POST, instance=self.article)
            if self.article_form.is_valid():
                self.article_form.save()
                return HttpResponseRedirect(reverse('home:article_default'))
                
        elif page is 'article_delete':
            self.delete_article(request.user)
            self.article =  get_object_or_404(Article, pk=article_id)
            self.article_form = ArticleConfirmForm(request.POST, instance=self.article)
            if self.article_form.is_valid():
                self.article.delete()
                return HttpResponseRedirect(reverse('home:article_default'))
                
        elif page is 'article_publish':
            self.new_article(request.user)
            self.edit_article(request.user)
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
        
