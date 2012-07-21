#!/usr/bin/env python
import urllib2
from lxml import etree
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from reddit.models import RedditArticle
from reddit.models import RedditComment
from reddit.models import Subreddit
import re

class Command(BaseCommand):
    def handle(self, *args, **options):
        self._scrape_subreddits()

    def _scrape_subreddits(self):
        subreddits_page_request = urllib2.Request('http://www.reddit.com/reddits')
        subreddits_page_handler = urllib2.urlopen(subreddits_page_request)
        subreddits_page_html = subreddits_page_handler.read()

        subreddits_html_parser = etree.HTMLParser(encoding='utf-8')
        subreddits_page = etree.HTML(article_html, subreddits_html_parser)
        
        subreddit_divs = page.xpath('//div[@class="entry likes"]')
        for subreddit_div in subreddit_divs:
            title_row = subreddit_div.xpath('p[@class="titlerow"]')[0]
            link = title_row.xpath('a')[0]
            url = link.get('href')
            
            title = etree.tostring(link, method='text', encoding='unicode')
            splits = re.split(":", title)
            name = split[0]

            description_div = subredd_div.xpath('//div[contains(@class, "description", true)]')
            description = etree.tostring(description_div, method="text", encoding="unicode")
            try:
                subreddit = Subreddit.objects.get(url=url)
                print subreddit + " already saved"
            except:
                subreddit = Subreddit(name=name, url=url, description=description)
                print subreddit
                subreddit.save()
