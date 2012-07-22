#!/usr/bin/env python
import urllib2
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from reddit.models import RedditArticle
from reddit.models import RedditComment
from reddit.models import Subreddit
import re
import json
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        if 'subreddits' in args:
            self._scrape_subreddits()
        elif 'articles' in args:
            self._scrape_articles()

    def _scrape_articles(self):
        front_page_request = urllib2.Request('https://www.reddit.com/.json', headers={'User-agent': 'pseudorandomstring'})
        front_page_request_handler = urllib2.urlopen(front_page_request)
        front_page_json = front_page_request_handler.read()
        front_page = json.loads(front_page_json)
        front_page = front_page['data']

        for article_dictionary in front_page['children']:
            article = article_dictionary['data']
            print article['name']
            
            try:
                previous = RedditArticle.objects.get(name=article['name'])
                next
            except:
                subreddit = Subreddit.objects.get(name=article['subreddit_id'])
                a = RedditArticle(domain=article['domain'],
                                  title=article['title'],
                                  score=article['score'],
                                  num_comments=article['num_comments'],
                                  created_utc=article['created_utc'],
                                  permalink=article['permalink'],
                                  url=article['url'],
                                  author=article['author'],
                                  name=article['name'],
                                  subreddit=subreddit)
                a.save()
        
        while 'after' in front_page:
            front_page_request = urllib2.Request('https://www.reddit.com/.json?after=' + front_page['after'], headers={'User-agent': 'pseudorandomstring'})
            front_page_request_handler = urllib2.urlopen(front_page_request)
            front_page_json = front_page_request_handler.read()
            front_page = json.loads(front_page_json)
            front_page = front_page['data']

            for article_dictionary in front_page['children']:
                article = article_dictionary['data']
                print article['name']

                try:
                    previous = RedditArticle.objects.get(name=article['name'])
                    next
                except:
                    subreddit = Subreddit.objects.get(name=article['subreddit_id'])
                    a = RedditArticle(domain=article['domain'],
                                      title=article['title'],
                                      score=article['score'],
                                      num_comments=article['num_comments'],
                                      created_utc=article['created_utc'],
                                      permalink=article['permalink'],
                                      url=article['url'],
                                      author=article['author'],
                                      name=article['name'],
                                      subreddit=subreddit)
                    a.save()
            time.sleep(5)

    def _scrape_subreddits(self):
        subreddits_page_request = urllib2.Request('http://www.reddit.com/reddits.json', headers={"User-agent": "pseudorandomstring"})
        
        subreddits_page_handler = urllib2.urlopen(subreddits_page_request)
        subreddits_json = subreddits_page_handler.read()
        subreddits = json.loads(subreddits_json)
        subreddits = subreddits['data']
        after = subreddits['after']
        
        for subreddit in subreddits['children']:
            subreddit = subreddit['data']
            try:
                s = Subreddit.objects.get(url=subreddit['url'])
            except:
                s = Subreddit(url=subreddit['url'],
                              name=subreddit['name'],
                              title=subreddit['title'],
                              description=subreddit['description'],
                              public_description=subreddit['public_description'],
                              reddit_id=subreddit['id'])
                s.save()
        
        time.sleep(5)
        
        while 'after' in subreddits:
            subreddits_page_request = urllib2.Request('http://www.reddit.com/reddits.json?after=' + subreddits['after'], headers={"User-agent": "pseudorandomstring"})
            subreddits_page_handler = urllib2.urlopen(subreddits_page_request)
            subreddits_json = subreddits_page_handler.read()
            subreddits = json.loads(subreddits_json)
            subreddits = subreddits['data']
            after = subreddits['after']
            
            for subreddit in subreddits['children']:
                subreddit = subreddit['data']
                try:
                    s = Subreddit.objects.get(url=subreddit['url'])
                except:
                    try:
                        s = Subreddit(url=subreddit['url'],
                                      name=subreddit['name'],
                                      title=subreddit['title'],
                                      description=subreddit['description'],
                                      public_description=subreddit['public_description'],
                                      reddit_id=subreddit['id'])
                        s.save()
                    except:
                        print subreddit
                        exit()

            time.sleep(5)
