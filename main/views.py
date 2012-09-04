from django.core.cache import cache
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from main.models import BwogArticle
from main.models import BwogComment
from django.db import connection
from django.utils import simplejson
from main.forms import ZeitgeistForm
from main.forms import CorrelationForm
from datetime import date, timedelta
import math


def index(request):
    return render_to_response('bwog/index.html')


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


def worst_daily_comments(request):
    d = date.today() - timedelta(days=1)
    try:
        worst_daily_comments = BwogComment.objects.filter(pub_date__gt=d).order_by('-downvotes')[:20]
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/worst.html', {'worst_comments': worst_daily_comments})


def best_comments(request):
    try:
        best_comments = BwogComment.objects.all().order_by('-upvotes')[:20]
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/best.html', {'best_comments': best_comments})


def best_daily_comments(request):
    d = date.today() - timedelta(days=1)
    try:
        best_daily_comments = BwogComment.objects.filter(pub_date__gt=d).order_by('-upvotes')[:20]
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/best.html', {'best_comments': best_daily_comments})


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
        comment_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment"])
        term1_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term2_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        both_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s AND body ILIKE %s", ['%' + term1 + '%', '%' + term2 + '%']])
        cache.set('comment_count', 1, 1)
        term1_prob = float(term1_count) / float(comment_count)
        term2_prob = float(term2_count) / float(comment_count)

        # misses time miss diff, hits times hit diff
        term1_variance = math.sqrt(((comment_count - term1_count) * (term1_prob) ** 2 + (term1_count) * (1 - term1_prob) ** 2) / comment_count)
        term2_variance = math.sqrt(((comment_count - term2_count) * (term2_prob) ** 2 + (term2_count) * (1 - term2_prob) ** 2) / comment_count)

        both_prob = float(both_count) / float(comment_count)
        term1_given_term2_prob = both_prob / term2_prob
        term2_given_term1_prob = both_prob / term1_prob
        independent_prob = term1_prob * term2_prob
        covariance = (both_prob - independent_prob)

        r = covariance / (term1_variance * term2_variance)
        r_squared = r * r

        result = {'term1': term1,
                  'term2': term2,
                  'term1_prob': term1_prob,
                  'term2_prob': term2_prob,
                  'term1_variance': term1_variance,
                  'term2_variance': term2_variance,
                  'term1_given_term2_prob': term1_given_term2_prob,
                  'term2_given_term1_prob': term2_given_term1_prob,
                  'joint_prob': both_prob,
                  'independent_joint_prob': independent_prob,
                  'covariance': covariance,
                  'ratio': both_prob / independent_prob,
                  'r': r,
                  'r_squared': r_squared}
        form = CorrelationForm(initial={'term1': term1, 'term2': term2})
        return render_to_response('bwog/correlation.html', {'res': result, 'form': form})


# private


def get_cache_string(select_array):
    if 1 != len(select_array):
        no_spaces = [select_array[0].replace(' ', '_'), [term.replace(' ', '_') for term in select_array[1]]]
        check_string = no_spaces[0] % tuple(no_spaces[1])
    else:
        no_spaces = [select_array[0].replace(' ', '_')]
        check_string = no_spaces[0]
    return check_string


def cache_count_select(db_connection, select_array):
    cache_string = get_cache_string(select_array)
    result = cache.get(cache_string)
    cursor = db_connection.cursor()
    if None == result:
        cursor.execute(*select_array)
        result = cursor.fetchone()[0]
        cache.set(cache_string, result, 24 * 60 * 60)
    return result
