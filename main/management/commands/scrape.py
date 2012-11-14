#!/usr/bin/env python
import urllib2
from lxml import etree
from bwog import BwogParser
import traceback
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        print "downloading"
        feed_url = "http://bwog.com/feed/"
        feed_request = urllib2.Request(feed_url)
        feed_request_handler = urllib2.urlopen(feed_request)
        unparsed_feed = feed_request_handler.read()

        print "parsing"
        sitemap = etree.XML(unparsed_feed)

        url_nodes = sitemap.xpath("//link")
        urls = [etree.tostring(url_node, method="text", encoding="unicode") for url_node in url_nodes]
        urls = urls[0:50]
        for bwog_url in urls:
            try:
                print bwog_url
                parser = BwogParser(bwog_url)
                article = parser.article
            except SystemExit as e:
                tb = traceback.format_exc()
                print tb
                print e
                exit()
            except KeyboardInterrupt as k:
                tb = traceback.format_exc()
                print tb
                print k
                exit()
            except:
                tb = traceback.format_exc()
                print tb
