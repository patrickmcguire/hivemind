import urllib2
import re
import os
import sys
from lxml import etree 
from lxml.etree import ElementTextIterator
from datetime import date
from datetime import datetime
from time import strptime
from pytz import timezone
from main.models import BwogArticle
from main.models import BwogComment
from django.db import models
from django.core.exceptions import ValidationError
import string

os.environ['TZ'] = 'America/New York'

class BwogParser:

    def __init__(self, url):
        self.url = url
        self.article = None
        self.comments = []
        self._parse()

    def _parseComments(self, page, bwog_internal_article_id):
        return self._recParseComments(page, bwog_internal_article_id);
    
    def _recParseComments(self, page, bwog_internal_article_id, depth = 1, parent_node = None):
        if parent_node == None:
            li_xpath_string = '//li[contains(concat(" ", @class, " "), " depth-1 ")]'
            comment_lis = page.xpath(li_xpath_string)
        else:
            xpath_string = 'ul/li[contains(concat(" ", @class, " "), " depth-{0} ")]'.format(depth)
            comment_lis = parent_node.xpath(xpath_string)

        parsed_comments = []
        for comment_li in comment_lis:
            comment_and_child_comments = self._commentLiParse(comment_li, depth, parent_node, bwog_internal_article_id)
            parsed_comments.extend(comment_and_child_comments)

        return parsed_comments

    def _commentLiParse(self, comment_li, depth, parent_node, bwog_internal_article_id):
        parsed_comments = []

        xpath_string = 'div[contains(concat(" ", @class, " "), " depth-{0} ")]'.format(depth)
        comment_div_candidates = comment_li.xpath(xpath_string)
        if 0 < len(comment_div_candidates):
            comment_div = comment_div_candidates[0]
            comment_id_string = comment_div.get('id')
            bwog_internal_id = comment_id_string[8:]
            
            comment_info_candidates = comment_div.xpath("div[@class='comment-info']")
            if 0 < len(comment_info_candidates):
                comment_info = comment_info_candidates[0]
                comment_author_candidates = comment_info.xpath('cite')
                link_candidates = comment_info.xpath('a')
                if (0 < len(comment_author_candidates)) and (0 == len(link_candidates)):
                    comment_author = etree.tostring(comment_author_candidates[0], method="text", encoding="unicode")
                elif 0 < len(link_cadidates):
                    link = link_candidates[0].text
                    comment_author = etree.tostring(link, method="text", encoding="unicode")
                    
                comment_meta_candidates = comment_info.xpath('span[@class="comment-meta commentmetadata"]')
                
                if -1 < len(comment_meta_candidates):
                    comment_meta = comment_meta_candidates[0]
                    
                    votes = comment_meta.xpath('span')
                    if 1 == len(votes): # administrator
                        comment_upvotes = 0
                        comment_downvotes = 0
                    else:
                        comment_upvote_span = votes[0]
                        comment_upvotes = int(comment_upvote_span.text)
                        comment_downvote_span = votes[1]
                        comment_downvotes = int(comment_downvote_span.text)
    
                    comment_time_candidates = comment_meta.xpath('a')
                    comment_time_div = comment_time_candidates[0]
                    # begins with \r\n for some reason
                    comment_time_string = comment_time_div.text
                    comment_time = comment_time_string[2:]
                    # 22 June 2012 at 2:24 pm
                    m = re.search('(\d+) (\w+) (\d+) at (\d+):(\d+) (am|pm)', comment_time)
                    year = int(m.group(3))
                    month = strptime(m.group(2), '%B').tm_mon
                    day = int(m.group(1))
                    hour = int(m.group(4))
                    minute = int(m.group(5))
                    am_pm = m.group(6)
                    if 'pm' == am_pm:
                        if 12 != hour:
                            hour += 12
                    elif 12 == hour:
                        hour -= 12

                    eastern = timezone("US/Eastern") 
                    comment_time = eastern.localize(datetime(year, month, day, hour, minute, 0))
                    
                    comment_track_hash_candidates = comment_meta.xpath('a')
                    last = len(comment_track_hash_candidates) - 1
                    comment_track_hash_div = comment_track_hash_candidates[last]
                    comment_track_hash = comment_track_hash_div.get('rel')

            body_xpath_string = "div[contains(@class, 'comment-info')=false]"
            potential_comment_body_divs = comment_div.xpath(body_xpath_string)
            if 0 < len(potential_comment_body_divs):
                comment_body_div = potential_comment_body_divs[0]
                paragraphs = comment_body_div.xpath("p")
            else:
                paragraphs = comment_div.xpath("p")
            
            comment_paragraphs = []
            for paragraph in paragraphs:
                    paragraph_text = paragraph.text
                    if None != paragraph_text:
                        comment_paragraphs.append(paragraph_text)
            comment_body = '\n\n'.join(comment_paragraphs)

            if None == comment_body:
                print self.url
                print bwog_internal_id
                raise Exception("No comment body!")
                exit()

        if None == parent_node:
            parent_bwog_internal_id = None
        else:
            id_string = parent_node.get('id')
            if None == id_string:
                parent_bwog_internal_id = None
            else:
                parent_bwog_internal_id = None
        
        try:
            int_bwog_article_id = int(bwog_internal_article_id)
            parent_article = BwogArticle.objects.get(bwog_id=int_bwog_article_id)
        except:
            print bwog_internal_article_id
            exit()
        
        if None == comment_author:
            print etree.tostring(comment_li, method="html", encoding="unicode")
            items = comment_li.xpath("div[@class='comment-info']") 
            for item in items:
                print "break"
                print etree.tostring(item)
                print "break"
            if 0 == len(items):
                print "somehow no items"
            exit()
    
        # processing
        comment_author = string.strip(comment_author)
        comment_body = string.string(comment_body)

        comment = BwogComment(author=comment_author,
                              body=comment_body,
                              pub_date=comment_time,
                              track_hash=comment_track_hash,
                              upvotes=comment_upvotes,
                              downvotes=comment_downvotes,
                              article=parent_article,
                              parent=None,
                              bwog_id=bwog_internal_id,
                              parent_bwog_id=parent_bwog_internal_id,
                              article_bwog_id=bwog_internal_article_id)
        comment.save()
        parsed_comments.append(comment)
        child_comments = self._recParseComments(comment_li, bwog_internal_article_id, depth + 1, comment_li)
        parsed_comments.extend(child_comments)
        return parsed_comments

    def _parse(self):
        article_request = urllib2.Request(self.url)
        article_request_handler = urllib2.urlopen(article_request)
        article_html = article_request_handler.read()

        hparser = etree.HTMLParser(encoding='utf-8')
        page = etree.HTML(article_html, hparser)

        potential_titles = page.xpath('//div[@class="post"]/h2/a')
        if 0 < len(potential_titles):
            title_node = potential_titles[0]
            article_title = title_node.text
        else:
            raise Exception("No title")

        potential_posts = page.xpath('//div[@class="post"]')
        if 0 < len(potential_posts):
            post = potential_posts[0]
            article_bwog_internal_id = post.get('id')
        else:
            raise Exception("No id")
        
        potential_bodies = page.xpath('//div[@class="contenttext"]')
        if 0 < len(potential_bodies):
            body_node = potential_bodies[0]
            article_body = etree.tostring(body_node, method="text", encoding="unicode")
        else:
            raise Exception("No body")

        url_slash_split = self.url.split("/")
        # http://bwog.com/(year)/(month)/(day)
        
        if 6 <= len(url_slash_split):
            year = int(url_slash_split[3])
            month = int(url_slash_split[4])
            day = int(url_slash_split[5])
            eastern = timezone("US/Eastern")
            article_date = eastern.localize(datetime(year, month, day))
        else:
            raise Exception("No date") 
        
        article = BwogArticle(url=self.url, 
                              title=article_title,
                              body=article_body,
                              pub_date=article_date,
                              bwog_id=article_bwog_internal_id)

        try:
            article.full_clean()
            article.save()
        except ValidationError as e:
            print self.url + " didn't work"
            print article_bwog_internal_id
            print e.message_dict
            body_node = potential_bodies[0]
            raise e
        except:
            e = sys.exc_info()[0]
            print e
            exit()

        comments = self._parseComments(page, article_bwog_internal_id)
        for comment in comments:
            try:
                if None != comment.parent_bwog_id:
                    id_to_find = int(comment.parent_bwog_id)
                    parent = BwogComment.objects.get(bwog_id=id_to_find)
                    comment.parent = parent
                    comment.save()
            except:
                print comment.parent_bwog_id
                exit()

        self.article = article
