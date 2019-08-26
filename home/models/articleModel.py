from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from home.models import Topic
from home.models import Publisher

class ArticleManager(models.Manager):
    def published_articles_list(self, *args, **kwargs):
        status = kwargs['status']
        articles = None
        if status:
            return self.all().filter(
                draft=False
            ).filter(publish_date_time__lte=timezone.now())
        else:
            return self.all().filter(publish_date_time=None)

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    publish_date_time= models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    draft = models.BooleanField(default=True)
    updated_date_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_date_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)
    ### image, height and width fields should be looked at
    image = models.ImageField(upload_to = upload_location,
        null = True,
        blank=True
    )

    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date_time', 'updated_date_time']
        permissions = (("publish_article", "Can publish an article"),)
