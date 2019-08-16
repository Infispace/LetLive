from django.urls import include 
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken import views as authviews
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
    path(r'auth/', include('rest_auth.urls')),
    path(r'api-token-auth/', authviews.obtain_auth_token),    
]
