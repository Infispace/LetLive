"""
/accounts/ urls.

For managing authenticated user accounts.
"""
from django.urls import path
from django.urls import include
from home.views import ProfileView
from home.views import RegistrationView
from home.forms import LoginForm
from home.forms import PasswordResetForm
from home.forms import PasswordChangeForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    # user profile view and edit
    path('profile/', include([
        path('', ProfileView.as_view(
            extra_context={'page': 'user_profile'}
        ), name='user_profile'),
        path('edit/', ProfileView.as_view(
            extra_context={'page': 'user_profile_edit'}
        ), name='user_profile_edit'),
    ])),
    # user register, login and logout
    path('register/', RegistrationView.as_view(
        extra_context={'page': 'signup'}
    ), name='user_register'),        
    path('logout/', auth_views.LogoutView.as_view(), name='user_logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='home/account_templates/login.html',
        authentication_form=LoginForm,
        extra_context={'page': 'login'},
        redirect_authenticated_user=True,
    ), name='user_login'),
    # user change password
    path('password_change/', include([
        path('', auth_views.PasswordChangeView.as_view(
            template_name='home/account_templates/account_base.html',
            form_class=PasswordChangeForm,
            success_url='/accounts/password_change/done/',
            extra_context={'page': 'password_change'}
        ), name='password_change'),
        path('done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='home/account_templates/account_base.html',
            extra_context={'page': 'password_change_done'}
        ), name='password_change_done'),
    ])),
    # user reset password
    path('password_reset/', include([
        path('', auth_views.PasswordResetView.as_view(
            template_name='home/account_templates/password_reset.html',
            form_class=PasswordResetForm,
            email_template_name='home/account_templates/password_reset_email.html'
        ), name='password_reset'),
        path('done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    ])),
    # user reset password finish
    path('reset/', include([
        path('<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ])),
]
