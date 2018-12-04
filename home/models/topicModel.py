from django.db import models

class Topic(models.Model):
    topic_name = models.CharField(max_length=250)
    intro = models.TextField()

    def __str__(self):
        return self.topic_name
