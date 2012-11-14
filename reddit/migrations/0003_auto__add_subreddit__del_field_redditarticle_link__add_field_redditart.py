# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subreddit'
        db.create_table('reddit_subreddit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.TextField')(default='')),
            ('name', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('reddit', ['Subreddit'])

        # Deleting field 'RedditArticle.link'
        db.delete_column('reddit_redditarticle', 'link')

        # Adding field 'RedditArticle.link_url'
        db.add_column('reddit_redditarticle', 'link_url',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'RedditArticle.subreddit'
        db.add_column('reddit_redditarticle', 'subreddit',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['reddit.Subreddit']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Subreddit'
        db.delete_table('reddit_subreddit')


        # User chose to not deal with backwards NULL issues for 'RedditArticle.link'
        raise RuntimeError("Cannot reverse this migration. 'RedditArticle.link' and its values cannot be restored.")
        # Deleting field 'RedditArticle.link_url'
        db.delete_column('reddit_redditarticle', 'link_url')

        # Deleting field 'RedditArticle.subreddit'
        db.delete_column('reddit_redditarticle', 'subreddit_id')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'url': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['reddit']