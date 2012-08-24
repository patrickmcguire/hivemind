#!/usr/bin/env python
import urllib2
from lxml import etree
from bwog import BwogParser
import traceback
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from main.models import BwogArticle
from main.models import BwogComment


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        print "downloading"
        sitemap_url = "http://www.bwog.com/sitemap.xml"
        sitemap_request = urllib2.Request(sitemap_url)
        sitemap_request_handler = urllib2.urlopen(sitemap_request)
        unparsed_sitemap = sitemap_request_handler.read()

        print "parsing"
        sitemap = etree.XML(unparsed_sitemap)

        url_nodes = sitemap.xpath("//*[local-name() = 'url']")
        url_nodes.pop(0)
        urls = []
        for node in url_nodes:
            possible_urls = node.xpath("*[local-name()='loc']")
            if len(possible_urls) > 0:
                url_node = possible_urls[0]
                url = url_node.text
                urls.append(url)

        for bwog_url in urls:
            try:
                article = BwogArticle.objects.get(url=bwog_url)
                print bwog_url + " already scraped"
                continue
            except:
                try:
                    parser = BwogParser(bwog_url)
                    article = parser.article
                    print article.url
                except SystemExit as e:
                    tb = traceback.format_exc()
                    print tb
                    exit()
                except KeyboardInterrupt as k:
                    tb = traceback.format_exc()
                    print tb
                    exit()
                except:
                    tb = traceback.format_exc()
                    print tb
