from django.urls import path, include
from django.views.generic import TemplateView

from .views.articleView import ArticleView
from .views.authView import UserLoginView
from .views.indexView import IndexView
from .views.topicView import TopicView
from .views.userView import UserView, userLogout

app_name = 'home'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/', include([
        path('', ArticleView.as_view(), {'page': 'my_blog'}, name='article_default'),
        path('new/', ArticleView.as_view(), {'page': 'article_new'}, name='article_new'),
        path('<int:article_id>/', ArticleView.as_view(), name='article'),
        path('<int:article_id>/edit/', ArticleView.as_view(), {'page': 'article_edit'}, name='article_edit'),
        path('<int:article_id>/delete/', ArticleView.as_view(), {'page': 'article_delete'}, name='article_delete'),
    ])),
    path('topic/', include([
        path('', TopicView.as_view(), name='topic_default'),
        path('new/', TopicView.as_view(), name='topic_new'),
        path('<int:topic_id>/', TopicView.as_view(), name='topic'),
        path('<int:topic_id>/edit/', TopicView.as_view(), name='topic_edit'),
        path('<int:topic_id>/delete/', TopicView.as_view(), name='topic_delete'),
    ])),
    path('user/', include([
        path('', UserView.as_view(), name='user_default'),
        path('<int:user_id>/', UserView.as_view(), name='user'),
        path('login/', UserLoginView.as_view(), name='user_login'),
        path('logout/', userLogout, name='user_logout'),
        path('register/', UserLoginView.as_view(), {'page': 'signup'}, name='user_register'),
        #path('password_reset/', UserView.as_view(), name='password_reset'),
    ])),
]
