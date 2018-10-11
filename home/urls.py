from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/', include([
        path('', views.ArticleView.as_view(), {'page': 'my_blog'}, name='article_default'),
        path('new/', views.ArticleView.as_view(), {'page': 'article_new'}, name='article_new'),
        path('<int:article_id>/', views.ArticleView.as_view(), name='article'),
        path('<int:article_id>/edit/', views.ArticleView.as_view(), {'page': 'article_edit'}, name='article_edit'),
        #path('<int:article_id>/delete/', views.ArticleView.as_view(), {'page': 'article_delete'}, name='article_delete'),
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
        path('register/', views.UserLoginView.as_view(), {'page': 'signup'}, name='user_register'),
        #path('password_reset/', views.UserView.as_view(), name='password_reset'),        
    ])),
]
