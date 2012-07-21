from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class RedditArticle(models.Model):
    url = models.TextField()
    link = models.TextField()
    title = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.title

class RedditComment(models.Model):
    author = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField('time published')
    points = models.IntegerField()
    article = models.ForeignKey(RedditArticle)
    parent = models.ForeignKey('self', null=True, blank=True)
    def __unicode__(self):
        return self.author
