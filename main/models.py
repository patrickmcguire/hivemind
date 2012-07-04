from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class BwogArticle(models.Model):
    url = models.TextField()
    title = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    bwog_id = models.BigIntegerField(unique=True)
    def __unicode__(self):
        return self.title

class BwogComment(models.Model):
    author = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField('time published')
    track_hash = models.TextField(null=True, blank=True)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    article = models.ForeignKey(BwogArticle)
    parent = models.ForeignKey('self', null=True, blank=True)
    bwog_id = models.BigIntegerField(unique=True)
    parent_bwog_id = models.BigIntegerField(null=True, blank=True)
    article_bwog_id = models.BigIntegerField()
    def __unicode__(self):
        return self.author

class ParsedItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.BigIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    tag = models.SlugField()
    word = models.TextField()
    sentence_sequence = models.SmallIntegerField()
    word_sequence = models.IntegerField()
    def __unicode__(self):
        return self.tag
