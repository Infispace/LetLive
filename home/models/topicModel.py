from django.db import models

class Topic(models.Model):
    topic_name = models.CharField(max_length=250, unique=True)
    intro = models.TextField()
    parent_topic = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        self.topic_name = self.topic_name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic_name
