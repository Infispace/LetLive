from django.db import models
from django.urls import reverse

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.username

class Topic(models.Model):
    topic_name = models.CharField(max_length=250)
    intro = models.TextField()

    def __str__(self):
        return self.topic_name


class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    article_height = models.IntegerField(default=0)
    article_width = models.IntegerField(default=0)

    def __str__(self):
        return self.headline




