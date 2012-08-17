#!/usr/bin/env python
import urllib2
import json
import time
from reddit.models import RedditArticle
from reddit.models import RedditComment
from reddit.models import Subreddit


class RedditRequest:
    def __init__(self, url, wait_time=60):
        self._url = url
        self._wait_time = wait_time

    def read(self):
        print self._url
        r = urllib2.Request(self._url, headers={'User-agent': 'pseudorandomstring'})
        handler = urllib2.urlopen(r)
        for i in range(1, 3):
            try:
                res = handler.read()
                time.sleep(self._wait_time)
                return res
            except:
                time.sleep(self._wait_time)


class RedditScraper:
    def __init__(self, root_url, wait_time=60):
        self._root_url = root_url
        self._wait_time = wait_time

    def _subreddit(self, subreddit_name, short_title):
        s = None
        try:
            s = Subreddit.objects.get(name=subreddit_name)
            return s
        except:
            search_url = 'http://www.reddit.com/reddits/search.json?q=' + short_title
            subreddit_result = RedditRequest(search_url, self._wait_time).read()
            search_dict = json.loads(subreddit_result)
            search_results = search_dict['data']['children']
            for potential_subreddit in search_results:
                potential_subreddit = potential_subreddit['data']
                if potential_subreddit['name'] == subreddit_name:
                    s = Subreddit(url=potential_subreddit['url'],
                                  name=potential_subreddit['name'],
                                  title=potential_subreddit['title'],
                                  description=potential_subreddit['description'],
                                  public_description=potential_subreddit['public_description'],
                                  reddit_id=potential_subreddit['id'])
                    s.save()
                    break
            return s

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

    def _scrape_article(self, article_model, article_url):
        article_page = RedditRequest(article_url, self._wait_time).read()
        article_comments = json.loads(article_page)
        art = article_comments.pop(0)
        article_model.body = art['data']['children'][0]['data']['selftext']
        article_model.save()
        for root_comment in article_comments[0]['data']['children']:
            self._rec_parse_comments(article_model, root_comment, None, 0)

    def scrape(self):
        front_page_json = RedditRequest(self._root_url, self._wait_time).read()
        front_page = json.loads(front_page_json)
        front_page = front_page['data']
        for article_dict in front_page['children']:
            try:
                article = RedditArticle.objects.get(name=article_dict['data']['name'])
            except:
                article = article_dict['data']
                subreddit = self._subreddit(article['subreddit_id'], article['subreddit'])
                if None != subreddit:
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
                                      subreddit=subreddit)
                    a.save()
                    article_url = 'http://reddit.com' + a.permalink + '.json'
                    self._scrape_article(a, article_url)
