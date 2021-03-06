# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BwogComment'
        db.create_table('main_bwogcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('track_hash', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')()),
            ('downvotes', self.gf('django.db.models.fields.IntegerField')()),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BwogArticle'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BwogComment'], null=True, blank=True)),
            ('bwog_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('parent_bwog_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('article_bwog_id', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('main', ['BwogComment'])


    def backwards(self, orm):
        # Deleting model 'BwogComment'
        db.delete_table('main_bwogcomment')


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