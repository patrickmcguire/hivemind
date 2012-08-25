from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from main.models import BwogArticle
from main.models import BwogComment
from django.db import connection
from django.utils import simplejson
from main.forms import ZeitgeistForm


def index(request):
    return HttpResponse("oh no")


def comment(request, comment_id):
    try:
        bwog_comment = BwogComment.objects.get(bwog_id=comment_id)
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/comment.html', {'comment': bwog_comment})


def worst_comments(request):
    try:
        worst_comments = BwogComment.objects.all().order_by('-downvotes')[:20]
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/worst.html', {'worst_comments': worst_comments})


def best_comments(request):
    try:
        best_comments = BwogComment.objects.all().order_by('-upvotes')[:20]
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/best.html', {'best_comments': best_comments})


def article(request, article_id):
    try:
        bwog_article = BwogArticle.objects.get(id=article_id)
    except BwogArticle.DoesNotExist:
        raise Http404
    return render_to_response('bwog/article.html', {'article': bwog_article})


def trend(request, term):
    cursor = connection.cursor()
    cursor.execute("SELECT EXTRACT(month from pub_date) as month, EXTRACT(year from pub_date) as year, COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s GROUP BY month, year ORDER BY year, month", ['%' + term + '%'])
    desc = cursor.description
    t1 = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    return HttpResponse(simplejson.dumps(t1), mimetype="application.json")


def zeitgeist(request):
    form = ZeitgeistForm()
    return render_to_response('bwog/zeitgeist.html', {'form': form})
