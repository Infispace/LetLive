from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:article_id>/', views.ArticleView.as_view(), name='article'),
    path('topic/<int:topic_id>/', views.TopicView.as_view(), name='topic'),
    path('user/<int:user_id>/', views.UserView.as_view(), name='user'),
]
