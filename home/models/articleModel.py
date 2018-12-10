from django.db import models
from django.urls import reverse
from django.utils import timezone
#from django.utils.safestring import mark_safe
#from markdown_deux import markdown

from .topicModel import Topic
from .userModel import Author, Publisher

# controls how the models work
class ArticleManager(models.Manager):
    def active(self, *args, **kwargs):
        #we override the default all(),i.e, (Article.objects.all())
        #Article.objects.all() = super(ArticleManager,self).all()
        return super(ArticleManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    publish_date= models.DateField(auto_now=False, auto_now_add=False)
    draft = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)
    # image, height and width fields should be looked at
    image = models.ImageField(upload_to = upload_location,
        null = True,
        blank=True
    )

    # linking the manager model to the model(Article) so that it can work
    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp', 'updated']
        permissions = (("publish_article", "Can publish an article"),)

    #def get_markdown(self):
        #content = self.content
        # converting content to markdown the django way
        #markdown_text = markdown(content)
        #return mark_safe(markdown_text)
