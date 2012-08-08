# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'RedditArticle.score'
        db.delete_column('reddit_redditarticle', 'score')

        # Adding field 'RedditArticle.ups'
        db.add_column('reddit_redditarticle', 'ups', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'RedditArticle.downs'
        db.add_column('reddit_redditarticle', 'downs', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding index on 'Subreddit', fields ['reddit_id']
        db.create_index('reddit_subreddit', ['reddit_id'])

        # Adding index on 'Subreddit', fields ['name']
        db.create_index('reddit_subreddit', ['name'])

        # Deleting field 'RedditComment.pub_date'
        db.delete_column('reddit_redditcomment', 'pub_date')

        # Adding field 'RedditComment.created_utc'
        db.add_column('reddit_redditcomment', 'created_utc', self.gf('django.db.models.fields.BigIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Removing index on 'Subreddit', fields ['name']
        db.delete_index('reddit_subreddit', ['name'])

        # Removing index on 'Subreddit', fields ['reddit_id']
        db.delete_index('reddit_subreddit', ['reddit_id'])

        # Adding field 'RedditArticle.score'
        db.add_column('reddit_redditarticle', 'score', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'RedditArticle.ups'
        db.delete_column('reddit_redditarticle', 'ups')

        # Deleting field 'RedditArticle.downs'
        db.delete_column('reddit_redditarticle', 'downs')

        # Adding field 'RedditComment.pub_date'
        db.add_column('reddit_redditcomment', 'pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2012, 8, 8)), keep_default=False)

        # Deleting field 'RedditComment.created_utc'
        db.delete_column('reddit_redditcomment', 'created_utc')


    models = {
        'reddit.redditarticle': {
            'Meta': {'object_name': 'RedditArticle'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'created_utc': ('django.db.models.fields.BigIntegerField', [], {}),
            'domain': ('django.db.models.fields.TextField', [], {}),
            'downs': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'num_comments': ('django.db.models.fields.IntegerField', [], {}),
            'permalink': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.Subreddit']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'ups': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        'reddit.redditcomment': {
            'Meta': {'object_name': 'RedditComment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.RedditArticle']"}),
            'author': ('django.db.models.fields.TextField', [], {}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_utc': ('django.db.models.fields.BigIntegerField', [], {}),
            'downs': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.RedditComment']", 'null': 'True', 'blank': 'True'}),
            'ups': ('django.db.models.fields.IntegerField', [], {})
        },
        'reddit.subreddit': {
            'Meta': {'object_name': 'Subreddit'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True', 'db_index': 'True'}),
            'public_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reddit_id': ('django.db.models.fields.TextField', [], {'unique': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['reddit']
