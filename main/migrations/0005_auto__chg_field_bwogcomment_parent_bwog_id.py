# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'BwogComment.parent_bwog_id'
        db.alter_column('main_bwogcomment', 'parent_bwog_id', self.gf('django.db.models.fields.BigIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'BwogComment.parent_bwog_id'
        db.alter_column('main_bwogcomment', 'parent_bwog_id', self.gf('django.db.models.fields.BigIntegerField')(default=None))

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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BwogComment']", 'null': 'True', 'blank': 'True'}),
            'parent_bwog_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'track_hash': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']