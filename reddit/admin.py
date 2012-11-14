from reddit.models import RedditArticle
from reddit.models import RedditComment
from reddit.models import Subreddit
from django.contrib import admin

admin.site.register(RedditArticle)
admin.site.register(RedditComment)
admin.site.register(Subreddit)
