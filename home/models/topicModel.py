from django.db import models

class Topic(models.Model):
    #: The topic name. It is unique.
    topic_name = models.CharField(max_length=250, unique=True)
    #: Brief intro about the topic
    intro = models.TextField()
    #: Timestamps
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    #: the parent topic. Relationship with `sub_topics`.
    parent_topic = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_topics'
    )

    def save(self, *args, **kwargs):
        self.topic_name = self.topic_name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic_name
