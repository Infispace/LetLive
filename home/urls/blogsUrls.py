"""
Web Aplication Urls.

Extents the urls from root directory.
Extents the urls from ``http:://domain/``.
"""
from django.urls import path
from django.urls import include
from home.views import BlogView


urlpatterns = [
    path('', BlogView.as_view(
        extra_context={'page': 'blog_default'},
    ), name='blog_default'),
    
    path('pending/', BlogView.as_view(
        extra_context={'page': 'blog_pending'},
    ), name='blog_pending'),
    
    path('published/', BlogView.as_view(
        extra_context={'page': 'blog_published'},
    ), name='blog_published'),
    
    path('<str:user_name>/', BlogView.as_view(
        extra_context={'page': 'blog_view'},
    ), name='blog_view'),
    
    path('edit/', BlogView.as_view(
        extra_context={'page': 'blog_edit'},
    ), name='blog_edit'),
]

