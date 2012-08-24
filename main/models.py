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

    @classmethod
    def get_text_extractor(self):
        return lambda model: model.body

    @classmethod
    def get_id_extractor(self):
        return lambda model: model.id
