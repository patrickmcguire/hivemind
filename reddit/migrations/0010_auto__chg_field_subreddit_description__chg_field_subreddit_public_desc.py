# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Subreddit.description'
        db.alter_column('reddit_subreddit', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Subreddit.public_description'
        db.alter_column('reddit_subreddit', 'public_description', self.gf('django.db.models.fields.TextField')(default=''))

        # Deleting field 'RedditComment.points'
        db.delete_column('reddit_redditcomment', 'points')

        # Adding field 'RedditComment.ups'
        db.add_column('reddit_redditcomment', 'ups', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'RedditComment.downs'
        db.add_column('reddit_redditcomment', 'downs', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Changing field 'Subreddit.description'
        db.alter_column('reddit_subreddit', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Subreddit.public_description'
        db.alter_column('reddit_subreddit', 'public_description', self.gf('django.db.models.fields.TextField')(null=True))

        # Adding field 'RedditComment.points'
        db.add_column('reddit_redditcomment', 'points', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Deleting field 'RedditComment.ups'
        db.delete_column('reddit_redditcomment', 'ups')

        # Deleting field 'RedditComment.downs'
        db.delete_column('reddit_redditcomment', 'downs')


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
            'downs': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reddit.RedditComment']", 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'ups': ('django.db.models.fields.IntegerField', [], {})
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
