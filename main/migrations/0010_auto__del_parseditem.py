# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ParsedItem'
        db.delete_table('main_parseditem')


    def backwards(self, orm):
        # Adding model 'ParsedItem'
        db.create_table('main_parseditem', (
            ('word', self.gf('django.db.models.fields.TextField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('tag', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('sentence_sequence', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('word_sequence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('main', ['ParsedItem'])


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
            'author': ('django.db.models.fields.TextField', [], {}),
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