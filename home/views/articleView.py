"""
:synopsis: View used to manage articles model.
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse
from home.models import Article
from home.forms import ArticleForm
from home.forms import ArticleConfirmForm

class ArticleView(PermissionRequiredMixin, TemplateView):
    #: The template to use for the view.
    template_name = 'home/article_templates/articles_base.html'
    #: The article to view
    article = None
    #: The article form to render
    article_form = None
    #: The error string to be rendered if any error
    error_string = None
    
    def get_permission_required(self):
        permission_required = []
        page = self.get_context_data()['page']

        if page == 'article_view':
            pass  # anyone can view articles
        elif page == 'article_publish':
            permission_required = ['home.publish_article']
        else:
            permission_required = [
                'home.add_article',
                'home.change_article',
                'home.delete_article',
            ]

        # permission against http method post
        # restrict to new, edit, delete and publish
        if self.request.method == 'POST' and page == 'article_view':
            raise PermissionDenied
            
        # return permissions
        return permission_required

    def get(self, request, article_id=0, *args, **kwargs,):
        page = self.get_context_data()['page']

        # get article by id
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)

        # get article forms
        if page == 'article_new':
            self.article_form = ArticleForm()
        elif page == 'article_edit':
            self.article_form = ArticleForm(instance=self.article)
        elif page == 'article_delete' or page == 'article_publish':
            self.article_form = ArticleConfirmForm(instance=self.article)
        
        # render template
        return self.render_to_response({
            'page': page,
            'article': self.article,
            'article_form': self.article_form,
        })

    def post(self, request, article_id=0, page='article', *args, **kwargs):
        page = self.get_context_data()['page']

        # get article by id
        if article_id != 0:
            self.article =  get_object_or_404(Article, pk=article_id)

        # get article forms
        if page == 'article_new':
            self.article_form = ArticleForm(request.POST)
        elif page == 'article_edit':
            self.article_form = ArticleForm(
                request.POST, 
                instance=self.article
            )
        elif page == 'article_delete' or page == 'article_publish':
            self.article_form = ArticleConfirmForm(
                request.POST, 
                instance=self.article
            )
            
        # make db changes
        success = False
        try:
            valid = self.article_form.is_valid()
            if valid and page == 'article_new':
                new_article = self.article_form.save(commit=False)
                new_article.author = request.user.author
                new_article.save()
                self.article_form.save_m2m()
            elif valid and page == 'article_edit':    
                self.article_form.save()
            elif valid and page == 'article_delete':
                self.article.delete()
            elif valid and page == 'article_publish':
                self.article.published = True
                self.article.save()

            success = True
        except Exception as e:
            success = False
            self.error_string = 'There was an error. Please try again.' 
            if settings.DEBUG:
                self.error_string = e
        
        # render template
        if success:
            return HttpResponseRedirect(reverse('home:blog_default'))

        return self.render_to_response({
            'page': page,
            'article': self.article,
            'article_form': self.article_form,
            'error_string': self.error_string
        })

