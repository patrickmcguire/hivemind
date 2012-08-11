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
import string

class Command(BaseCommand):
    def handle(self, *args, **options):
        if 'subreddits' in args:
            self._scrape_subreddits()
        elif 'articles' in args:
            self._scrape_articles()

    def _scrape_articles(self):
        front_page_request = urllib2.Request('http://www.reddit.com/.json', headers={'User-agent': 'pseudorandomstring'})
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
                s = None
                try:              
                    s = Subreddit.objects.get(name=article['subreddit_id'])
                except:
                    subreddit_name = article['subreddit']
                    search_url = 'http://www.reddit.com/reddits/search.json?q=' + subreddit_name
                    subreddit_search_request = urllib2.Request(search_url, headers={'User-agent': 'pseudorandomstring'})
                    subreddit_search_request_handler = urllib2.urlopen(subreddit_search_request)
                    subreddit_search_request_result = None
                    try:
                        subreddit_search_request_result = subreddit_search_request_handler.read()
                    except:
                        time.sleep(60)
                        try:
                            subreddit_search_request_result = subreddit_search_request_handler.read()
                        except:
                            next
                    subreddit_decoded = json.loads(subreddit_search_request_result)
                    subreddit_search_data = subreddit_decoded['data']
                    subreddit_search_results = subreddit_search_data['children']
                    for potential_subreddit in subreddit_search_results:
                        subreddit = potential_subreddit['data']
                        if subreddit['name'] == article['subreddit_id']:
                            s = Subreddit(url=subreddit['url'],
                                        name=subreddit['name'],
                                        title=subreddit['title'],
                                        description=subreddit['description'],
                                        public_description=subreddit['public_description'],
                                        reddit_id=subreddit['id'])
                            s.save()

                a = RedditArticle(domain=article['domain'],
                                  title=article['title'],
                                  ups=article['ups'],
                                  downs=article['downs'],
                                  num_comments=article['num_comments'],
                                  created_utc=article['created_utc'],
                                  permalink=article['permalink'],
                                  url=article['url'],
                                  author=article['author'],
                                  name=article['name'],
                                  subreddit=s)
                a.save()

                article_url = 'http://reddit.com' + a.permalink + '.json'
                print article_url
                article_request = urllib2.Request(article_url, headers={'User-agent': 'pseudorandomstring'})
                article_request_handler = urllib2.urlopen(article_request)
                article_json = article_request_handler.read()
                article_comments = json.loads(article_json)
                art = article_comments.pop(0) 
                a.body = art['data']['children'][0]['data']['selftext']
                a.save()
                
                root_comments = article_comments[0]
                for root_comment in article_comments[0]['data']['children']:
                    self._rec_parse_comments(a, root_comment, None, 0)
                time.sleep(60)
        
        while 'after' in front_page:
            front_page_request = urllib2.Request('http://www.reddit.com/.json?after=' + front_page['after'], headers={'User-agent': 'pseudorandomstring'})
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
                s = None
                try:              
                    s = Subreddit.objects.get(name=article['subreddit_id'])
                except:
                    subreddit_name = article['subreddit']
                    search_url = 'http://www.reddit.com/reddits/search.json?q=' + subreddit_name
                    subreddit_search_request = urllib2.Request(search_url, headers={'User-agent': 'pseudorandomstring'})
                    subreddit_search_request_handler = urllib2.urlopen(subreddit_search_request)
                    subreddit_search_request_result = subreddit_search_request_handler.read()
                    subreddit_decoded = json.loads(subreddit_search_request_result)
                    subreddit_search_data = subreddit_decoded['data']
                    subreddit_search_results = subreddit_search_data['children']
                    for potential_subreddit in subreddit_search_results:
                        subreddit = potential_subreddit['data']
                        if subreddit['name'] == article['subreddit_id']:
                            s = Subreddit(url=subreddit['url'],
                                        name=subreddit['name'],
                                        title=subreddit['title'],
                                        description=subreddit['description'],
                                        public_description=subreddit['public_description'],
                                        reddit_id=subreddit['id'])
                            s.save()

                a = RedditArticle(domain=article['domain'],
                                  title=article['title'],
                                  ups=article['ups'],
                                  downs=article['downs'],
                                  num_comments=article['num_comments'],
                                  created_utc=article['created_utc'],
                                  permalink=article['permalink'],
                                  url=article['url'],
                                  author=article['author'],
                                  name=article['name'],
                                  subreddit=s)
                a.save()
                time.sleep(5)

                article_url = 'http://reddit.com' + a.url + '.json'
                article_request = urllib2.Request(article_url, headers={'User-agent': 'pseudorandomstring'})
                article_request_handler = urllib2.urlopen(article_request)
                article_comments = None
                try:
                    article_json = article_request_handler.read()
                    article_comments = json.loads(article_json)
                except:
                    time.sleep(60)
                    try:
                        article_json = article_request_handler.read()
                        article_comments = json.loads(article_json)
                    except:
                        next
                
                if None != article_comments:
                    art = article_comments.pop(0) # don't want the first
                    a.body = art['data']['children'][0]['data']['selftext']
                    a.save()
                    
                    for child in article_comments['data']['children']:
                        self._rec_parse_commente(a, child, None)
                    
                else:
                    print "No comments found"
            time.sleep(60)
    
    def _rec_parse_comments(self, article, comment, parent, depth):
        comment_dict = comment['data']
        if comment['kind'] == 'more':
            return
        comment_model = RedditComment(author=comment_dict['author'],
                                      body=comment_dict['body'],
                                      created_utc=comment_dict['created_utc'],
                                      ups=comment_dict['ups'],
                                      downs=comment_dict['downs'],
                                      article=article,
                                      parent=parent)
        comment_model.save()

        replies = comment_dict['replies']
        if not isinstance(replies, basestring):
            children = replies['data']['children']
            tab = ""
            for i in range(0, depth):
                tab += "\t"
            print tab + str(len(children))
            for c in children:
                self._rec_parse_comments(article, c, comment_model, depth + 1)


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
        
        time.sleep(60)
        
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

            time.sleep(60)
