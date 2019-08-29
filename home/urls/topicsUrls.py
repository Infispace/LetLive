"""
/topics/ urls.

For managing topics.
"""
from django.urls import path
from django.urls import include
from home.views import TopicView


urlpatterns = [
    path('', TopicView.as_view(
        extra_context={'page': 'topic_default'}
    ), name='topic_default'),
    
    path('new/', TopicView.as_view(
        extra_context={'page': 'topic_new'}
    ), name='topic_new'),
    
    path('<int:topic_id>/', TopicView.as_view(
        extra_context={'page': 'topic_view'}
    ), name='topic_view'),
    
    path('<int:topic_id>/edit/', TopicView.as_view(
        extra_context={'page': 'topic_edit'}
    ), name='topic_edit'),
    
    path('<int:topic_id>/delete/', TopicView.as_view(
        extra_context={'page': 'topic_delete'}
    ), name='topic_delete'),
]

