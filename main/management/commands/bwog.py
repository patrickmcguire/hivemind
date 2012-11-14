import urllib2
import re
import os
import sys
from lxml import etree
from datetime import datetime
from time import strptime
from pytz import timezone
from main.models import BwogArticle
from main.models import BwogComment
from django.core.exceptions import ValidationError
import string

os.environ['TZ'] = 'America/New York'


class BwogParser:

    def __init__(self, url):
        self.url = url
        self.article = None
        self.comments = []
        self._parse()

    def _parseComments(self, page, bwog_article_id):
        return self._recParseComments(page, bwog_article_id)

    def _recParseComments(self, page, bwog_article_id, depth=1, parent_node=None):
        print depth
        if parent_node is None:
            li_xpath_string = '//li[contains(concat(" ", @class, " "), " depth-1 ")]'
            comment_lis = page.xpath(li_xpath_string)
        else:
            xpath_string = 'ul/li[contains(concat(" ", @class, " "), " depth-{0} ")]'.format(depth)
            comment_lis = parent_node.xpath(xpath_string)

        parsed_comments = []
        for comment_li in comment_lis:
            comment_and_child_comments = self._commentLiParse(comment_li, depth, parent_node, bwog_article_id)
            parsed_comments.extend(comment_and_child_comments)

        return parsed_comments

    def _commentLiParse(self, comment_li, depth, parent_node, bwog_article_id):
        parsed_comments = []

        xpath_string = 'div[contains(concat(" ", @class, " "), " depth-{0} ")]'.format(depth)
        comment_div_candidates = comment_li.xpath(xpath_string)
        if 0 < len(comment_div_candidates):
            comment_div = comment_div_candidates[0]
            comment_id_string = comment_div.get('id')
            bwog_internal_id = comment_id_string[12:]

            comment_author_candidates = comment_div.xpath("div[@class='comment-author vcard']")
            if 0 < len(comment_author_candidates):
                comment_author_div = comment_author_candidates[0]
                cite = comment_author_div.xpath('cite')[0]
                comment_author = etree.tostring(cite, method="text", encoding="unicode")

            comment_meta_candidates = comment_div.xpath("div[@class='comment-meta datetime']")
            if 0 < len(comment_meta_candidates):
                comment_meta_div = comment_meta_candidates[0]
                up_spans = comment_meta_div.xpath("span[@data-voting-direction='up']")
                if 0 < len(up_spans):  # not an administrator
                    up_span = up_spans[0]
                    up_count_span = up_span.xpath("span[@class='like-count']")[0]
                    comment_upvotes = int(etree.tostring(up_count_span, method="text", encoding="unicode"))

                down_spans = comment_meta_div.xpath("span[@data-voting-direction='down']")
                if 0 < len(down_spans):  # not an administrator
                    down_span = down_spans[0]
                    down_count_span = down_span.xpath("span[@class='dislike-count']")[0]
                    comment_downvotes = int(etree.tostring(down_count_span, method="text", encoding="unicode"))

                date_div = comment_meta_div.xpath('a')[0]
                date_text = etree.tostring(date_div, method="text", encoding="unicode")
                date_text = date_text.strip()
                # 22 June 2012 @ 2:24 pm
                # September 23, 2012 @ 2:24 pm
                m = re.search('(\w+) (\d+), (\d+) @ (\d+):(\d+) (am|pm)', date_text)
                year = int(m.group(3))
                month = strptime(m.group(1), '%B').tm_mon
                day = int(m.group(2))
                hour = int(m.group(4))
                minute = int(m.group(5))
                am_pm = m.group(6)
                if 'pm' == am_pm:
                    if 12 != hour:
                        hour += 12
                elif 'am' == am_pm and 12 == hour:
                    hour -= 12

                eastern = timezone("US/Eastern")
                comment_time = eastern.localize(datetime(year, month, day, hour, minute, 0))

            comment_mod_candidates = comment_div.xpath('div[@class="comment-mod"]')
            if 0 < len(comment_mod_candidates):
                comment_mod_div = comment_mod_candidates[0]
                track_link = comment_mod_div.xpath('a')[0]
                comment_track_hash = track_link.get('rel')

            comment_body = None
            xpath_string = 'div[contains(concat(" ", @class, " "), " reg-comment-body ")]'
            comment_body_candidates = comment_div.xpath(xpath_string)
            if 0 < len(comment_body_candidates):
                comment_body = comment_body_candidates[0]
                comment_body = etree.tostring(comment_body, method="text", encoding="unicode")

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
            int_bwog_article_id = int(bwog_article_id)
            parent_article = BwogArticle.objects.get(id=int_bwog_article_id)
        except:
            print bwog_article_id
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
        comment_body = string.strip(comment_body)

        comment = None
        try:
            comment = BwogComment.objects.get(bwog_id=bwog_internal_id)
            comment.body = comment_body
            comment.upvotes = comment_upvotes
            comment.downvotes = comment_downvotes
        except:
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
                                  article_bwog_id=None)
        comment.save()
        parsed_comments.append(comment)
        child_comments = self._recParseComments(comment_li, bwog_article_id, depth + 1, comment_li)
        parsed_comments.extend(child_comments)
        return parsed_comments

    def _parse(self):
        article_request = urllib2.Request(self.url)
        article_request.add_header('User-Agent', 'BwogStatsBot')
        article_request_handler = urllib2.urlopen(article_request)
        article_html = article_request_handler.read()

        hparser = etree.HTMLParser(encoding='utf-8')
        page = etree.HTML(article_html, hparser)

        potential_titles = page.xpath('//div[@class="post-title"]/a')
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
            article_bwog_internal_id = None

        potential_bodies = page.xpath('//div[@class="post-content"]')
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

        article = None
        try:
            article = BwogArticle.objects.get(url=self.url)
        except:
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

        comments = self._parseComments(page, article.id)
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
