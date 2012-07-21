#!/usr/bin/env python
import urllib2
from lxml import etree
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from reddit.models import RedditArticle
from reddit.models import RedditComment

class Command(BaseCommand):
    def handle(self, *app_lables, **options):
        print 
