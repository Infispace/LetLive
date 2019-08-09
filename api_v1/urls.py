from django.urls import include 
from django.urls import path
from rest_framework import routers
from api_v1 import views

app_name = 'api_v1'

#routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'subscribers', views.SubscriberViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('rest_framework.urls', 'api_v1')),
]
