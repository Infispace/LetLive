"""
Web Aplication Urls.

Extents the urls from root directory.
Extents the urls from ``http:://domain/``.
"""
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from home.views import ArticleView
from home.views import IndexView
from home.views import TopicView
from home.views import ProfileView
from home.views import UsersView
from home.views import PublishView
from home.views import RegistrationView
from home.forms import LoginForm
from home.forms import PasswordResetForm
from home.forms import PasswordChangeForm


app_name = 'home'

#: :page: Represents the page to be shown used by the Templates.
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    # `/users/` for managing users
    path('users/', include([
        path('', UsersView.as_view(), {'page': 'user_default'}, name='user_default'),
        path('new/', UsersView.as_view(), {'page': 'user_new'}, name='user_new'),
        path('authors/', UsersView.as_view(), {'page': 'user_author'}, name='user_author'),
        path('publishers/', UsersView.as_view(), {'page': 'user_publisher'}, name='user_publisher'),
        path('<int:user_id>/', UsersView.as_view(), {'page': 'user_view'}, name='user_view'),
        path('<int:user_id>/delete/', UsersView.as_view(), {'page': 'user_delete'}, name='user_delete'),
    ])),
    # `/account/` for managing user accounts
    path('accounts/', include([
        # user profile view and edit
        path('profile/', include([
            path('', ProfileView.as_view(), {'page': 'user_profile'}, name='user_profile'),
            path('edit/', ProfileView.as_view(), {'page': 'user_profile_edit'}, name='user_profile_edit'),
        ])),
        # user register, login and logout
        path('register/', RegistrationView.as_view(), {'page': 'signup'}, name='user_register'),        
        path('logout/', auth_views.LogoutView.as_view(), name='user_logout'),
        path('login/', auth_views.LoginView.as_view(
            template_name='home/login.html',
            authentication_form=LoginForm,
            extra_context={'page': 'login'},
            redirect_authenticated_user=True,
        ), name='user_login'),
        # user change password
        path('password_change/', include([
            path('', auth_views.PasswordChangeView.as_view(
                template_name='home/account.html',
                form_class=PasswordChangeForm,
                success_url='/accounts/password_change/done/',
                extra_context={'page': 'password_change'}
            ), name='password_change'),
            path('done/', auth_views.PasswordChangeDoneView.as_view(
                template_name='home/account.html',
                extra_context={'page': 'password_change_done'}
            ), name='password_change_done'),
        ])),
        # user reset password
        path('password_reset/', include([
            path('', auth_views.PasswordResetView.as_view(
                template_name='home/password_reset.html',
                form_class=PasswordResetForm,
                email_template_name='home/password_reset_email.html'
            ), name='password_reset'),
            path('done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        ])),
        # user reset password finish
        path('reset/', include([
            path('<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
            path('done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
        ])),
    ])),
    path('articles/', include([
        path('', ArticleView.as_view(), {'page': 'my_blog'}, name='article_default'),
        path('<int:article_id>/', ArticleView.as_view(), name='article'),
        path('<int:article_id>/edit/', ArticleView.as_view(), {'page': 'article_edit'}, name='article_edit'),
        path('<int:article_id>/delete/', ArticleView.as_view(), {'page': 'article_delete'}, name='article_delete'),
        path('<int:article_id>/publish/', ArticleView.as_view(), {'page': 'article_publish'}, name='article_publish'),
        path('filter/<str:filter>/', ArticleView.as_view(), {'page': 'article_filter'}, name='article_filter'),
        path('new/view', ArticleView.as_view(), {'page': 'article_new_view'}, name='article_new_view'),
        path('new/', ArticleView.as_view(), {'page': 'article_new'}, name='article_new'),
    ])),
    path('topics/', include([
        path('', TopicView.as_view(), {'page': 'topic_default'}, name='topic_default'),
        path('new/', TopicView.as_view(), {'page': 'topic_new'}, name='topic_new'),
        path('<int:topic_id>/', TopicView.as_view(), name='topic'),
        path('<int:topic_id>/edit/', TopicView.as_view(), {'page': 'topic_edit'}, name='topic_edit'),
        path('<int:topic_id>/delete/', TopicView.as_view(), {'page': 'topic_delete'}, name='topic_delete'),
    ])),
    path('publishers/', include([
        path('', PublishView.as_view(), {'page': 'publish_article'}, name='publish_article'),
        path('<int:article_id>/', PublishView.as_view(), name='publish_article_id'),
    ])),
    path('blogs/', include([
        path('<str:user_name>/', ArticleView.as_view(), {'page': 'blog'}, name='user_blog'),
        #path('<str:user_name>/edit/'),
    ])),
]
