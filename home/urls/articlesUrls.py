"""
/articles/ urls.

For managing authenticated articles.
"""
from django.urls import path
from django.urls import include
from home.views import ArticleView


urlpatterns = [
    #path('', ArticleView.as_view(
    #    extra_context={'page': 'article_default'},
    #), name='article_default'),
    
    path('<int:article_id>/', ArticleView.as_view(
        extra_context={'page': 'article_view'},
    ), name='article_view'),
    
    path('<int:article_id>/edit/', ArticleView.as_view(
        extra_context={'page': 'article_edit'},
    ), name='article_edit'),
    
    path('<int:article_id>/delete/', ArticleView.as_view(
        extra_context={'page': 'article_delete'},
    ), name='article_delete'),
    
    path('<int:article_id>/publish/', ArticleView.as_view(
        extra_context={'page': 'article_publish'},
    ), {'page': 'article_publish'}, name='article_publish'),
    
    path('new/', ArticleView.as_view(
        extra_context={'page': 'article_new'},
    ), {'page': 'article_new'}, name='article_new'),
]

