# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BwogComment'
        db.delete_table('main_bwogcomment')


    def backwards(self, orm):
        # Adding model 'BwogComment'
        db.create_table('main_bwogcomment', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BwogComment'], null=True, blank=True)),
            ('parent_bwog_id', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('bwog_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.BwogArticle'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article_bwog_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('track_hash', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')()),
            ('downvotes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['BwogComment'])


    models = {
        'main.bwogarticle': {
            'Meta': {'object_name': 'BwogArticle'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'bwog_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['main']