from django.contrib import admin
from .models.articleModel import Article
from .models.topicModel import Topic
from .models.userModel import Author, Publisher, Admin

admin.site.register(Article)
admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Admin)
