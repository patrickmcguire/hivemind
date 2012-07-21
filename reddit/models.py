from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Subreddit(models.Model):
    url = models.TextField(default="")
    name = models.TextField(default="")
    description = models.TextField(default="")

class RedditArticle(models.Model):
    url = models.TextField()
    link_url = models.TextField(default="")
    title = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    subreddit = models.ForeignKey(Subreddit)
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
