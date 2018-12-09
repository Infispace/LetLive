from django.contrib import admin
from .models.articleModel import Article
from .models.userModel import Author, Publisher, Admin

admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Admin)
