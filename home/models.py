from django.conf import settings # to get the default auth_user
from django.db import models
from django.urls import reverse
from django.utils import timezone
<<<<<<< HEAD
#from markdown_deux import markdown
=======
from markdown_deux import markdown
>>>>>>> dev
from django.utils.safestring import mark_safe

# controls how the models work
class ArticleManager(models.Manager):
    def active(self, *args, **kwargs):
        #we override the default all(),i.e, (Article.objects.all())
        #Article.objects.all() = super(ArticleManager,self).all()
        return super(ArticleManager, self).filter(draft=False).filter(publish__lte=timezone.now())


class Topic(models.Model):
    topic_name = models.CharField(max_length=250)
    intro = models.TextField()

    def __str__(self):
        return self.topic_name

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to = upload_location,
                              null = True,
                              blank=True,
                              width_field = "width_field",
<<<<<<< HEAD
                              height_field= "height_field")
=======
                              height_field= "heigth_field")
>>>>>>> dev
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    publish= models.DateField(auto_now=False, auto_now_add=False)
    draft = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

<<<<<<< HEAD
    # linking the manager model to the model(Article) so that it can work
=======
    # linking th manager model to the model(Article) so that it can work
>>>>>>> dev
    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp', 'updated']

<<<<<<< HEAD
    #def get_markdown(self):
        #content = self.content
        # converting content to markdown the django way
        #markdown_text = markdown(content)
        #return mark_safe(markdown_text)
=======
    def get_markdown(self):
        content = self.content
        # converting content to markdown the django way
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
>>>>>>> dev
