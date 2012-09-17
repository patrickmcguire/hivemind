from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

# Examples:
# url(r'^$', 'hivemindio.views.home', name='home'),
# url(r'^hivemindio/', include('hivemindio.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bwog/$', 'main.views.index'),
    url(r'^bwog/comments/(?P<comment_id>\d+)/$', 'main.views.comment'),
    url(r'^bwog/comments/worst/$', 'main.views.worst_comments'),
    url(r'^bwog/comments/best/$', 'main.views.best_comments'),
    url(r'^bwog/comments/daily_best/$', 'main.views.best_daily_comments'),
    url(r'^bwog/comments/daily_worst/$', 'main.views.worst_daily_comments'),
    url(r'^bwog/articles/(?P<article_id>\d+)/$', 'main.views.article'),
    url(r'^bwog/articles/(?P<article_id>\d+)/comments/$', 'main.views.article_comments'),
    url(r'^bwog/trend/(?P<term>[A-Za-z0-9"\'-* ]+)/$', 'main.views.trend'),
    url(r'^bwog/zeitgeist/$', 'main.views.zeitgeist'),
    url(r'^bwog/correlation/$', 'main.views.correlation'),
    url(r'^bwog/versus/$', 'main.views.versus'),
    url(r'^$', 'main.views.index'),
    url(r'^bwog/predictions/$', 'main.views.predictions'),
    url(r'^privacy.txt', 'django.views.generic.simple.direct_to_template', {'template': 'bwog/privacy.txt'}),
    url(r'^test', 'django.views.generic.simple.direct_to_template', {'template': 'bwog/index2.html'}),
    url(r'^google09e6491b8ce4f523.html', 'django.views.generic.simple.direct_to_template', {'template': 'bwog/google09e6491b8ce4f523.html'})
)

