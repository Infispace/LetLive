"""
Web Aplication Urls.

Extents the urls from root directory.
Extents the urls from ``http:://domain/``.
"""
from django.urls import path
from django.urls import include
from home.views import ArticleView
from home.views import UsersView
from home.views import PublishView


urlpatterns = [
    path('articles/', include([
        path('', ArticleView.as_view(), {'page': 'my_blog'}, name='article_default'),
        path('<int:article_id>/', ArticleView.as_view(), name='article'),
        path('<int:article_id>/edit/', ArticleView.as_view(), {'page': 'article_edit'}, name='article_edit'),
        path('<int:article_id>/delete/', ArticleView.as_view(), {'page': 'article_delete'}, name='article_delete'),
        path('<int:article_id>/publish/', ArticleView.as_view(), {'page': 'article_publish'}, name='article_publish'),
        path('filter/<str:filter>/', ArticleView.as_view(), {'page': 'article_filter'}, name='article_filter'),
        path('new/view', ArticleView.as_view(), {'page': 'article_new_view'}, name='article_new_view'),
        path('new/', ArticleView.as_view(), {'page': 'article_new'}, name='article_new'),
    ])),
    path('publishers/', include([
        path('', PublishView.as_view(), {'page': 'publish_article'}, name='publish_article'),
        path('<int:article_id>/', PublishView.as_view(), name='publish_article_id'),
    ])),
    path('blogs/', include([
        path('<str:user_name>/', ArticleView.as_view(), {'page': 'blog'}, name='user_blog'),
        #path('<str:user_name>/edit/'),
    ])),
]
