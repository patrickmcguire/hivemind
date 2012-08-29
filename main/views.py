from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from main.models import BwogArticle
from main.models import BwogComment
from django.db import connection
from django.utils import simplejson
from main.forms import ZeitgeistForm
from main.forms import CorrelationForm
from datetime import date
from django.core.cache import cache


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
    cursor.execute("SELECT EXTRACT(month from pub_date) as month, EXTRACT(year from pub_date) as year, COUNT(*) FROM main_bwogcomment WHERE  body ILIKE %s GROUP BY month, year ORDER BY year, month", ['%' + term + '%'])
    desc = cursor.description
    t1 = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    formatted = []
    for d in t1:
        formatted.append((int(date(int(d['year']), int(d['month']), 1).strftime("%s")) * 1000, d['count']))
    return HttpResponse(simplejson.dumps(formatted), mimetype="application.json")


def zeitgeist(request):
    params = request.GET
    possible = ['term1', 'term2', 'term3', 'term4']
    prefilled = {}
    for term in possible:
        if term in params:
            prefilled[term] = params[term]
    form = ZeitgeistForm(initial=prefilled)
    return render_to_response('bwog/zeitgeist.html', {'form': form})


def correlation(request):
    params = request.GET
    if not ('term1' in params and 'term2' in params):
        form = CorrelationForm()
        return render_to_response('bwog/correlation.html', {'res': False, 'form': form})
    else:
        term1 = params['term1']
        term2 = params['term2']
        cursor = connection.cursor()
        all_count_string = "count:"
        comment_count = cache.get(all_count_string)
        if None == comment_count:
            cursor.execute("SELECT COUNT(*) FROM main_bwogcomment")
            comment_count = cursor.fetchone()[0]
            cache.set(all_count_string, comment_count, 24 * 60 * 60)

        term1_cache_string = "count:" + "_".join(term1.split(" "))
        term1_count = cache.get(term1_cache_string)
        if None == term1_count:
            cursor.execute("SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%'])
            term1_count = cursor.fetchone()[0]
            cache.set(term1_cache_string, term1_count, 24 * 60 * 60)

        term2_cache_string = "count:" + "_".join(term2.split(" "))
        term2_count = cache.get(term2_cache_string)
        if None == term2_count:
            cursor.execute("SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%'])
            term2_count = cursor.fetchone()[0]
            cache.set(term2_cache_string, term2_count, 24 * 60 * 60)

        both_cache_string = "count:" + "_".join(term1.split(" ")) + "count:" + "_".join(term2.split(" "))
        both_count = cache.get(both_cache_string)
        if None == both_count:
            cursor.execute("SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s AND body ILIKE %s", ['%' + term1 + '%', '%' + term2 + '%'])
            both_count = cursor.fetchone()[0]
            cache.set(both_cache_string, both_count, 24 * 60 * 60)

        term1_prob = float(term1_count) / float(comment_count)
        term2_prob = float(term2_count) / float(comment_count)
        both_prob = float(both_count) / float(comment_count)
        term1_given_term2_prob = both_prob / term2_prob
        term2_given_term1_prob = both_prob / term1_prob
        independent_prob = term1_prob * term2_prob
        covariance = both_prob - independent_prob
        result = {'term1': term1, 'term2': term2, 'term1_prob': term1_prob, 'term2_prob': term2_prob, 'term1_given_term2_prob': term1_given_term2_prob, 'term2_given_term1_prob': term2_given_term1_prob, 'joint_prob': both_prob, 'independent_joint_prob': independent_prob, 'covariance': covariance, 'ratio': both_prob / independent_prob}
        form = CorrelationForm(initial={'term1': term1, 'term2': term2})
        return render_to_response('bwog/correlation.html', {'res': result, 'form': form})
