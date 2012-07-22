# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subreddit.title'
        db.add_column('reddit_subreddit', 'title',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Subreddit.public_description'
        db.add_column('reddit_subreddit', 'public_description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Subreddit.reddit_id'
        db.add_column('reddit_subreddit', 'reddit_id',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Subreddit.title'
        db.delete_column('reddit_subreddit', 'title')

        # Deleting field 'Subreddit.public_description'
        db.delete_column('reddit_subreddit', 'public_description')

        # Deleting field 'Subreddit.reddit_id'
        db.delete_column('reddit_subreddit', 'reddit_id')


    models = {
        'reddit.redditarticle': {
            'Meta': {'object_name': 'RedditArticle'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_url': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.Subreddit']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'reddit.redditcomment': {
            'Meta': {'object_name': 'RedditComment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.RedditArticle']"}),
            'author': ('django.db.models.fields.TextField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.RedditComment']", 'null': 'True', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'reddit.subreddit': {
            'Meta': {'object_name': 'Subreddit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'public_description': ('django.db.models.fields.TextField', [], {}),
            'reddit_id': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['reddit']