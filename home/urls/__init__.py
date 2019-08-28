"""
Web Aplication Urls.

Extents the urls from root directory.
Extents the urls from ``http:://domain/``.

:page: Represents the page to be shown used by the Templates.
       Should be passed as extra_conrext to the class based views.
"""
from django.urls import path
from django.urls import include
from home.views import IndexView

app_name = 'home'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path(r'accounts/', include('home.urls.accountsUrls')),
    path(r'topics/', include('home.urls.topicsUrls')),
    path(r'users/', include('home.urls.usersUrls')),
    path(r'', include('home.urls.otherUrls')),
]
