# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RedditArticle.body'
        db.delete_column('reddit_redditarticle', 'body')

        # Deleting field 'RedditArticle.link_url'
        db.delete_column('reddit_redditarticle', 'link_url')

        # Deleting field 'RedditArticle.pub_date'
        db.delete_column('reddit_redditarticle', 'pub_date')

        # Adding field 'RedditArticle.domain'
        db.add_column('reddit_redditarticle', 'domain',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'RedditArticle.score'
        db.add_column('reddit_redditarticle', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'RedditArticle.num_comments'
        db.add_column('reddit_redditarticle', 'num_comments',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'RedditArticle.created_utc'
        db.add_column('reddit_redditarticle', 'created_utc',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'RedditArticle.permalink'
        db.add_column('reddit_redditarticle', 'permalink',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'RedditArticle.author'
        db.add_column('reddit_redditarticle', 'author',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'RedditArticle.name'
        db.add_column('reddit_redditarticle', 'name',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'RedditArticle.body'
        db.add_column('reddit_redditarticle', 'body',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'RedditArticle.link_url'
        db.add_column('reddit_redditarticle', 'link_url',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'RedditArticle.pub_date'
        db.add_column('reddit_redditarticle', 'pub_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 22, 0, 0)),
                      keep_default=False)

        # Deleting field 'RedditArticle.domain'
        db.delete_column('reddit_redditarticle', 'domain')

        # Deleting field 'RedditArticle.score'
        db.delete_column('reddit_redditarticle', 'score')

        # Deleting field 'RedditArticle.num_comments'
        db.delete_column('reddit_redditarticle', 'num_comments')

        # Deleting field 'RedditArticle.created_utc'
        db.delete_column('reddit_redditarticle', 'created_utc')

        # Deleting field 'RedditArticle.permalink'
        db.delete_column('reddit_redditarticle', 'permalink')

        # Deleting field 'RedditArticle.author'
        db.delete_column('reddit_redditarticle', 'author')

        # Deleting field 'RedditArticle.name'
        db.delete_column('reddit_redditarticle', 'name')


    models = {
        'reddit.redditarticle': {
            'Meta': {'object_name': 'RedditArticle'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'created_utc': ('django.db.models.fields.BigIntegerField', [], {}),
            'domain': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'num_comments': ('django.db.models.fields.IntegerField', [], {}),
            'permalink': ('django.db.models.fields.TextField', [], {}),
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