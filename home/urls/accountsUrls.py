"""
/accounts/ urls.

For managing authenticated user accounts.
"""
from django.urls import path
from django.urls import include
from django.urls import reverse
from home.views import ProfileView
from home.views import RegistrationView
from home.views import SubscriptionView
from home.forms import LoginForm
from home.forms import PasswordResetForm
from home.forms import PasswordChangeForm
from home.forms import SetPasswordForm
from django.contrib.auth import views as auth_views


# user profile view and edit
profile_urlpatterns = [
    path('', ProfileView.as_view(
        extra_context={'page': 'user_profile'}
    ), name='user_profile'),
    
    path('edit/', ProfileView.as_view(
        extra_context={'page': 'user_profile_edit'}
    ), name='user_profile_edit'),
]

# user change password
password_change_urlpatterns = [
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
]

# user reset password
password_reset_urlpatterns = [
    path('', auth_views.PasswordResetView.as_view(
        form_class=PasswordResetForm,
        success_url='/accounts/password_reset/done/',
        template_name='home/account_templates/password_reset.html',
        email_template_name='home/account_templates/password_reset_email.txt',
        html_email_template_name='home/account_templates/password_reset_email.html',
    ), name='password_reset'),
    
    path('done/', auth_views.PasswordResetDoneView.as_view(
        template_name='home/account_templates/password_reset_done.html',
    ), name='password_reset_done'),
]

# user reset password finish
password_reset_finish_urlpatterns = [
    path('<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=SetPasswordForm,
        success_url='/accounts/reset/done/',
        template_name='home/account_templates/password_reset_confirm.html',
    ), name='password_reset_confirm'),
    
    path('done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='home/account_templates/password_reset_complete.html',
    ), name='password_reset_complete'),
]

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='home/account_templates/login.html',
        authentication_form=LoginForm,
        extra_context={'page': 'login'},
        redirect_authenticated_user=True,
    ), name='user_login'),
    
    path('register/', RegistrationView.as_view(
        extra_context={'page': 'signup'}
    ), name='user_register'), 
    
    path('subscription/', SubscriptionView.as_view(
        extra_context={'page': 'user_subscription'}
    ), name='user_subscription'),
    
    path('logout/', auth_views.LogoutView.as_view(
    ), name='user_logout'),
    
    path('password_change/', include(password_change_urlpatterns)),
    path('password_reset/', include(password_reset_urlpatterns)),
    path('reset/', include(password_reset_finish_urlpatterns)),
    path('profile/', include(profile_urlpatterns)),
]

