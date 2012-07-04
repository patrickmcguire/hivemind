# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BwogArticle.url'
        db.add_column('main_bwogarticle', 'url',
                      self.gf('django.db.models.fields.TextField')(default='http://bwog.com'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BwogArticle.url'
        db.delete_column('main_bwogarticle', 'url')


    models = {
        'main.bwogarticle': {
            'Meta': {'object_name': 'BwogArticle'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'bwog_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'main.bwogcomment': {
            'Meta': {'object_name': 'BwogComment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BwogArticle']"}),
            'article_bwog_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'author': ('django.db.models.fields.TextField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'bwog_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BwogComment']"}),
            'parent_bwog_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'track_hash': ('django.db.models.fields.TextField', [], {}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']