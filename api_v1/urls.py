"""
Api Version 1 Urls.

Extents the urls from ``http:://domain/api_v1/``.
"""
from rest_framework.authtoken import views as authviews
from rest_framework import routers
from django.urls import include 
from django.urls import path
from api_v1 import views

app_name = 'api_v1'

#routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'subscribers', views.SubscriberViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'publishers', views.PublisherViewSet)
router.register(r'admins', views.AdminViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'topics', views.TopicViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'auth/', include([
        path(r'', include('rest_auth.urls')),
        path(r'registration/', include('rest_auth.registration.urls')),
        path(r'api-token/', authviews.obtain_auth_token, name='rest_api_token'),
    ])),  
]
