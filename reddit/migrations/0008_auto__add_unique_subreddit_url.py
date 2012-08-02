# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Subreddit', fields ['url']
        db.create_unique('reddit_subreddit', ['url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Subreddit', fields ['url']
        db.delete_unique('reddit_subreddit', ['url'])


    models = {
        'reddit.redditarticle': {
            'Meta': {'object_name': 'RedditArticle'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'created_utc': ('django.db.models.fields.BigIntegerField', [], {}),
            'domain': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'num_comments': ('django.db.models.fields.IntegerField', [], {}),
            'permalink': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'public_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reddit_id': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['reddit']