from django.urls import path, include
from django.views.generic import TemplateView

from .views import ArticleView
from .views import UserLoginView
from .views import user_logout
from .views import IndexView
from .views import TopicView
from .views import ProfileView
from .views import UsersView
from .views import PublishView

app_name = 'home'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('publish/', include([
        path('', PublishView.as_view(), {'page': 'publish_article'}, name='publish_article'),
        path('<int:article_id>/', PublishView.as_view(), name='publish_article_id'),
    ])),
    path('article/', include([
        path('', ArticleView.as_view(), {'page': 'my_blog'}, name='article_default'),
        path('filter/<str:filter>/', ArticleView.as_view(), {'page': 'article_filter'}, name='article_filter'),
        path('new/', ArticleView.as_view(), {'page': 'article_new'}, name='article_new'),
        path('<int:article_id>/', ArticleView.as_view(), name='article'),
        path('<int:article_id>/edit/', ArticleView.as_view(), {'page': 'article_edit'}, name='article_edit'),
        path('<int:article_id>/delete/', ArticleView.as_view(), {'page': 'article_delete'}, name='article_delete'),
        path('<int:article_id>/publish/', ArticleView.as_view(), {'page': 'article_publish'}, name='article_publish'),
    ])),
    path('topic/', include([
        path('', TopicView.as_view(), {'page': 'topic_default'}, name='topic_default'),
        path('new/', TopicView.as_view(), {'page': 'topic_new'}, name='topic_new'),
        path('<int:topic_id>/', TopicView.as_view(), name='topic'),
        path('<int:topic_id>/edit/', TopicView.as_view(), {'page': 'topic_edit'}, name='topic_edit'),
        path('<int:topic_id>/delete/', TopicView.as_view(), {'page': 'topic_delete'}, name='topic_delete'),
    ])),
    path('account/', include([
        path('', ProfileView.as_view(), {'page': 'user_default'}, name='user_default'),
        path('<int:user_id>/', ProfileView.as_view(), {'page': 'user_view'}, name='user_view'),
        path('<int:user_id>/delete/', UsersView.as_view(), {'page': 'user_delete'}, name='user_delete'),
        path('login/', UserLoginView.as_view(), name='user_login'),
        path('logout/', user_logout, name='user_logout'),
        path('register/', UserLoginView.as_view(), {'page': 'signup'}, name='user_register'),
        #path('password_reset/', ProfileView.as_view(), name='password_reset'),
    ])),
    path('users/', include([
        path('', UsersView.as_view(), name='users_default'),
        path('<str:user_level>/', UsersView.as_view(), {'users': 'filter'}, name='users_filter_level'),
        path('<str:user_level>/new/', UsersView.as_view(), {'users': 'new'}, name='users_new'),
        #path('<int:user_id>/delete/', UsersView.as_view(), {'users': 'delete'}, name='user_delete'),
    ]), {'page': 'users'}),
]
