from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/', include([
        path('', views.ArticleView.as_view(), name='article_default'),
        path('<int:article_id>/', views.ArticleView.as_view(), name='article'),
    ])),
    path('topic/', include([
        path('', views.TopicView.as_view(), name='topic_default'),
        path('<int:topic_id>/', views.TopicView.as_view(), name='topic'),
    ])),
    path('user/', include([
        path('', views.UserView.as_view(), name='user_default'),
        path('<int:user_id>/', views.UserView.as_view(), name='user'),
        path('login/', views.UserLoginView.as_view(), name='user_login'),
        path('logout/', views.UserView.userLogout, name='user_logout'),
        path('logout/', views.UserView.as_view(), name='password_reset'),
    ])),
]
