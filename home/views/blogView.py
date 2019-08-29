"""
:synopsis: View used to manage articles model.
"""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.urls import reverse
from home.models import Article
from home.forms import ArticleForm
from home.forms import ArticleConfirmForm

class BlogView(PermissionRequiredMixin, TemplateView):
    #: The template to use for the view.
    template_name = 'home/blog.html'
    #: The list of articles to display
    article_list = None
    
    def get_permission_required(self):
        permission_required = [
            'home.add_article',
            'home.change_article',
            'home.delete_article',
        ]

        # permission against http method post
        if self.request.method == 'POST':
            raise PermissionDenied

        # return permissions
        return permission_required

    def get(self, request, *args, **kwargs,):
        page = self.get_context_data()['page']
        
        # get articles list
        if page == 'blog_pending':
            self.article_list = Article.objects.published(False)
        elif page == 'blog_published':
            self.article_list = Article.objects.published()
        
        return self.render_to_response({
            'page': page,
            'article_list': self.article_list,
        })

    def post(self, request, *args, **kwargs):
        page = self.get_context_data()['page']

        return self.render_to_response({
            'page': page,
            'article_list': self.article_list,
        })
        
