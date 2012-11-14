from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Subreddit(models.Model):
    url = models.TextField(unique=True)
    name = models.TextField(unique=True, db_index=True)
    title = models.TextField()
    description = models.TextField(blank=True)
    public_description = models.TextField(blank=True)
    reddit_id = models.TextField(unique=True, db_index=True)
    def __unicode__(self):
        return self.url

class RedditArticle(models.Model):
    domain = models.TextField()
    title = models.TextField()
    body = models.TextField(null=True, blank=True)
    ups = models.IntegerField()
    downs = models.IntegerField()
    num_comments = models.IntegerField()
    created_utc = models.BigIntegerField()
    permalink = models.TextField(unique=True)
    url = models.TextField()
    author = models.TextField()
    name = models.TextField(unique=True)
    subreddit = models.ForeignKey(Subreddit, db_index=True)
    def __unicode__(self):
        return self.title

class RedditComment(models.Model):
    author = models.TextField()
    body = models.TextField()
    created_utc = models.BigIntegerField()
    ups = models.IntegerField()
    downs = models.IntegerField()
    article = models.ForeignKey(RedditArticle, db_index=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    def __unicode__(self):
        return self.author
