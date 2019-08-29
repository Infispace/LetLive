"""
/users/ urls.

For managing users.
"""
from django.urls import path
from django.urls import include
from home.views import UsersView


urlpatterns = [
    path('', UsersView.as_view(
         extra_context={'page': 'user_default'}
    ), name='user_default'),
    
    path('new/', UsersView.as_view(
        extra_context={'page': 'user_new'}
    ), name='user_new'),
    
    path('authors/', UsersView.as_view(
        extra_context={'page': 'user_author'}
    ), name='user_author'),
    
    path('publishers/', UsersView.as_view(
        extra_context={'page': 'user_publisher'}
    ), name='user_publisher'),
    
    path('<int:user_id>/', UsersView.as_view(
        extra_context={'page': 'user_view'}
    ), name='user_view'),
    
    path('<int:user_id>/delete/', UsersView.as_view(
        extra_context={'page': 'user_delete'}
    ), name='user_delete'),
]

