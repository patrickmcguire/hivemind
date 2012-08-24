#!/usr/bin/env python
import urllib2
from django.core.management.base import BaseCommand
from reddit.models import Subreddit
from scrape import RedditScraper
import json
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        if 'subreddits' in args:
            self._scrape_subreddits()
        if 'frontpage' in args:
            self._scrape_frontpage()
        if 'all_subreddits' in args:
            l = len(args)
            last = args[l-1]
            if last != 'all_subreddits':
                self._scrape_all(last)
            else:
                self._scrape_all()


    def _scrape_frontpage(self):
        frontpage_url = 'http://www.reddit.com/.json'
        RedditScraper(frontpage_url).scrape()

    def _scrape_all(self, start=None):
        reached = False
        for subreddit in Subreddit.objects.all():
            if None != start:
                print 'did ' + subreddit.url
                if start == subreddit.url or reached:
                    reached = True
                    url = 'http://www.reddit.com' + subreddit.url + '.json'
                    print url
                    RedditScraper(url).scrape()
                if not reached:
                    next
            else:
                url = 'http://www.reddit.com' + subreddit.url + '.json'
                print url
                RedditScraper(url).scrape()

    def _scrape_subreddits(self):
        subreddits_page_request = urllib2.Request('http://www.reddit.com/reddits.json', headers={"User-agent": "hivemindio"})

        subreddits_page_handler = urllib2.urlopen(subreddits_page_request)
        subreddits_json = subreddits_page_handler.read()
        subreddits = json.loads(subreddits_json)
        subreddits = subreddits['data']
        # after = subreddits['after']

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

        time.sleep(60)

        while 'after' in subreddits:
            subreddits_page_request = urllib2.Request('http://www.reddit.com/reddits.json?after=' + subreddits['after'], headers={"User-agent": "pseudorandomstring"})
            subreddits_page_handler = urllib2.urlopen(subreddits_page_request)
            subreddits_json = subreddits_page_handler.read()
            subreddits = json.loads(subreddits_json)
            subreddits = subreddits['data']
            # after = subreddits['after']

            for subreddit in subreddits['children']:
                subreddit = subreddit['data']
                print subreddit['url']
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

            time.sleep(60)
