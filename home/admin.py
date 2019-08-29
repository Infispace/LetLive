"""
Register the Web application models with Django admin.

The models registered are

* home.models.articleModel.Article
* home.models.topicModel.Topic
* home.models.userModel.Author
* home.models.userModel.Admin
* home.models.userModel.Subscriber
"""
from django.contrib import admin
from home.models.articleModel import Article
from home.models.topicModel import Topic
from home.models.userModel import Author
from home.models.userModel import Admin
from home.models.userModel import Subscriber

admin.site.register(Article)
admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Admin)
admin.site.register(Subscriber)
