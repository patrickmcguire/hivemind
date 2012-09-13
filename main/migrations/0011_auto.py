# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'BwogComment', fields ['author']
        db.create_index('main_bwogcomment', ['author'])


    def backwards(self, orm):
        # Removing index on 'BwogComment', fields ['author']
        db.delete_index('main_bwogcomment', ['author'])


    models = {
        'main.bwogarticle': {
            'Meta': {'object_name': 'BwogArticle'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'bwog_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'main.bwogcomment': {
            'Meta': {'object_name': 'BwogComment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BwogArticle']"}),
            'article_bwog_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'author': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'bwog_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BwogComment']", 'null': 'True', 'blank': 'True'}),
            'parent_bwog_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'track_hash': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']