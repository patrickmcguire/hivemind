from django.core.cache import cache
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from main.models import BwogArticle
from main.models import BwogComment
from django.db import connection
from django.utils import simplejson
from main.forms import ZeitgeistForm, CorrelationForm, PredictionForm
from datetime import date, timedelta
import nltk
from nltk import ngrams
import math
import redis


class GRAM_CLASS:
    UP = 1
    DOWN = 2


def index(request):
    return render_to_response('bwog/index.html', context_instance=RequestContext(request))


def comment(request, comment_id):
    try:
        bwog_comment = BwogComment.objects.get(bwog_id=comment_id)
    except BwogComment.DoesNotExist:
        raise Http404
    return render_to_response('bwog/comment.html', {'comment': bwog_comment}, context_instance=RequestContext(request))


def worst_comments(request):
    try:
        worst_comments = BwogComment.objects.all().order_by('-downvotes')[:21]
    except BwogComment.DoesNotExist:
        raise Http404
    worst_comments = get_ranked_hash(worst_comments, lambda comment: comment.downvotes)
    return render_to_response('bwog/ranked.html', {
        'description': 'Worst Comments',
        'timeframe': 'All Time',
        'rank_unit': 'Downvotes',
        'ranked_comments': worst_comments}, context_instance=RequestContext(request))


def worst_daily_comments(request):
    d = date.today() - timedelta(days=1)
    try:
        worst_daily_comments = BwogComment.objects.filter(pub_date__gt=d).order_by('-downvotes')[:21]
    except BwogComment.DoesNotExist:
        raise Http404
    worst_daily_comments = get_ranked_hash(worst_comments, lambda comment: comment.downvotes)
    return render_to_response('bwog/ranked.html', {
        'description': 'Worst Comments',
        'timeframe': 'Today',
        'rank_unit': 'Downvotes',
        'ranked_comments': worst_daily_comments
    })


def best_comments(request):
    try:
        best_comments = BwogComment.objects.all().order_by('-upvotes')[:21]
    except BwogComment.DoesNotExist:
        raise Http404
    best_comments = get_ranked_hash(best_comments, lambda comment: comment.upvotes)
    return render_to_response('bwog/ranked.html', {
        'description': 'Best Comments',
        'timeframe': 'All Time',
        'rank_unit': 'Upvotes',
        'ranked_comments': best_comments
    })


def best_daily_comments(request):
    d = date.today() - timedelta(days=1)
    try:
        best_daily_comments = BwogComment.objects.filter(pub_date__gt=d).order_by('-upvotes')[:21]
    except BwogComment.DoesNotExist:
        raise Http404
    best_daily_comments = get_ranked_hash(best_comments, lambda comment: comment.upvotes)
    return render_to_response('bwog/ranked.html', {
        'description': 'Best Comments',
        'timeframe': 'Today',
        'rank_unit': 'Upvotes',
        'ranked_comments': best_daily_comments
    })


def article(request, article_id):
    try:
        bwog_article = BwogArticle.objects.get(id=article_id)
    except BwogArticle.DoesNotExist:
        raise Http404
    return render_to_response('bwog/article.html', {'article': bwog_article}, context_instance=RequestContext(request))


def trend(request, term):
    cursor = connection.cursor()
    cursor.execute("SELECT EXTRACT(month from pub_date) as month, EXTRACT(year from pub_date) as year, COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s GROUP BY month, year ORDER BY year, month", ['%' + term + '%'])
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
    return render_to_response('bwog/zeitgeist.html', {'form': form}, context_instance=RequestContext(request))


def predictions(request):
    params = request.GET
    if not ('comment_text' in params):
        form = PredictionForm()
        return render_to_response('bwog/prediction.html', {'res': False, 'form': form})
    else:
        text = params['comment_text']
        tokens = nltk.word_tokenize(text)
        grams = ngrams(tokens, 3)
        upvotes = 0.0
        downvotes = 0.0
        for gram in grams:
            upvotes += gram_weight(gram, GRAM_CLASS.UP)
            print upvotes
            downvotes += gram_weight(gram, GRAM_CLASS.DOWN)
            print downvotes
        form = PredictionForm(initial={'comment_text': text})
        print downvotes
        print upvotes
        return render_to_response('bwog/prediction.html', {'res': True, 'form': form, 'downvotes': downvotes, 'upvotes': upvotes}, context_instance=RequestContext(request))


def correlation(request):
    params = request.GET
    if not ('term1' in params and 'term2' in params):
        form = CorrelationForm()
        return render_to_response('bwog/correlation.html', {'res': False, 'form': form})
    else:
        term1 = params['term1']
        term2 = params['term2']
        comment_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment"])
        term1_upvotes = cache_count_select(connection, ["SELECT SUM(upvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term1_downvotes = cache_count_select(connection, ["SELECT SUM(downvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term2_upvotes = cache_count_select(connection, ["SELECT SUM(upvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        term2_downvotes = cache_count_select(connection, ["SELECT SUM(downvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        term1_worst_body = cache_count_select(connection, ["SELECT id FROM main_bwogcomment WHERE downvotes = (SELECT max(downvotes) from main_bwogcomment where body ILIKE %s)", ['%' + term1 + '%']])
        term1_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term2_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        both_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s AND body ILIKE %s", ['%' + term1 + '%', '%' + term2 + '%']])
        cache.set('comment_count', 1, 1)
        term1_average_upvotes = float(term1_upvotes) / float(term1_count)
        term1_average_downvotes = float(term1_downvotes) / float(term1_downvotes)
        term2_average_upvotes = float(term2_upvotes) / float(term2_count)
        term2_average_downvotes = float(term2_downvotes) / float(term2_downvotes)

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

        term1_prob_pretty = round((float(term1_prob) * 100), 2)
        term2_prob_pretty = round((float(term2_prob) * 100), 2)
        term1_variance_pretty = round((float(term1_variance) * 100), 2)
        term2_variance_pretty = round((float(term2_variance) * 100), 2)
        both_prob_pretty = round((float(both_prob) * 100), 4)
        term1_given_term2_prob_pretty = round((float(term1_given_term2_prob) * 100), 2)
        term2_given_term1_prob_pretty = round((float(term2_given_term1_prob) * 100), 2)
        independent_prob_pretty = round((float(independent_prob) * 100), 3)
        ratio_pretty = round((float(both_prob / independent_prob)), 1)
        r_squared_pretty = round((float(r_squared) * 100), 3)
        covariance_pretty = round((float((both_prob - independent_prob)) * 100), 3)

        result = {'term1': term1,
                  'term2': term2,
                  'term1_count': term1_count,
                  'term2_count': term2_count,
                  'both_count': both_count,
                  'term1_prob': term1_prob_pretty,
                  'term2_prob': term2_prob_pretty,
                  'term1_variance': term1_variance_pretty,
                  'term2_variance': term2_variance_pretty,
                  'term1_average_upvotes': round((term1_average_upvotes), 2),
                  'term2_average_upvotes': round((term2_average_upvotes), 2),
                  'term1_average_score': round((term1_average_upvotes - term1_average_downvotes), 2),
                  'term2_average_score': round((term2_average_upvotes - term2_average_downvotes), 2),
                  'term1_average_downvotes': round((term1_average_downvotes), 2),
                  'term2_average_downvotes': round((term2_average_downvotes), 2),
                  'term1_given_term2_prob': term1_given_term2_prob_pretty,
                  'term2_given_term1_prob': term2_given_term1_prob_pretty,
                  'term1_prob_pretty': term1_prob_pretty,
                  'term2_prob_pretty': term2_prob_pretty,
                  'joint_prob': both_prob_pretty,
                  'independent_joint_prob': independent_prob_pretty,
                  'covariance': covariance_pretty,
                  'ratio': ratio_pretty,
                  'r': r,
                  'term1_upvotes': term1_upvotes,
                  'term2_upvotes': term2_upvotes,
                  'term1_worst_body': term1_worst_body,
                  'r_squared': round((r_squared), 2)}
        form = CorrelationForm(initial={'term1': term1, 'term2': term2})
        return render_to_response('bwog/correlation.html', {'res': result, 'form': form}, context_instance=RequestContext(request))


def versus(request):
    params = request.GET
    if not ('term1' in params and 'term2' in params):
        form = CorrelationForm()
        return render_to_response('bwog/versus.html', {'res': False, 'form': form})
    else:
        term1 = params['term1']
        term2 = params['term2']
        comment_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment"])
        term1_upvotes = cache_count_select(connection, ["SELECT SUM(upvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term1_downvotes = cache_count_select(connection, ["SELECT SUM(downvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term2_upvotes = cache_count_select(connection, ["SELECT SUM(upvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        term2_downvotes = cache_count_select(connection, ["SELECT SUM(downvotes) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        term1_worst_body = cache_count_select(connection,["SELECT id FROM main_bwogcomment WHERE downvotes = (SELECT max(downvotes) from main_bwogcomment where body ILIKE %s)", ['%' + term1 + '%']])
        term1_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term1 + '%']])
        term2_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s", ['%' + term2 + '%']])
        both_count = cache_count_select(connection, ["SELECT COUNT(*) FROM main_bwogcomment WHERE body ILIKE %s AND body ILIKE %s", ['%' + term1 + '%', '%' + term2 + '%']])
        cache.set('comment_count', 1, 1)
        term1_average_upvotes = float(term1_upvotes) / float(term1_count)
        term1_average_downvotes = float(term1_downvotes) / float(term1_count)
        term2_average_upvotes = float(term2_upvotes) / float(term2_count)
        term2_average_downvotes = float(term2_downvotes) / float(term2_count)

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

        term1_prob_pretty = round((float(term1_prob) * 100), 2)
        term2_prob_pretty = round((float(term2_prob) * 100), 2)
        term1_variance_pretty = round((float(term1_variance) * 100), 2)
        term2_variance_pretty = round((float(term2_variance) * 100), 2)
        both_prob_pretty = round((float(both_prob) * 100), 4)
        term1_given_term2_prob_pretty = round((float(term1_given_term2_prob) * 100), 2)
        term2_given_term1_prob_pretty = round((float(term2_given_term1_prob) * 100), 2)
        independent_prob_pretty = round((float(independent_prob) * 100), 3)
        ratio_pretty = round((float(both_prob / independent_prob)), 1)
        r_squared_pretty = round((float(r_squared) * 100), 3)
        covariance_pretty = round((float((both_prob - independent_prob)) * 100), 3)

        result = {'term1': term1,
                  'term2': term2,
                  'term1_count': term1_count,
                  'term2_count': term2_count,
                  'both_count': both_count,
                  'term1_prob': term1_prob_pretty,
                  'term2_prob': term2_prob_pretty,
                  'term1_average_upvotes': round((term1_average_upvotes), 2),
                  'term2_average_upvotes': round((term2_average_upvotes), 2),
                  'term1_average_score': round((term1_average_upvotes - term1_average_downvotes), 2),
                  'term2_average_score': round((term2_average_upvotes - term2_average_downvotes), 2),
                  'term1_average_downvotes': round((term1_average_downvotes), 2),
                  'term2_average_downvotes': round((term2_average_downvotes), 2),
                  'term1_given_term2_prob': term1_given_term2_prob_pretty,
                  'term2_given_term1_prob': term2_given_term1_prob_pretty,
                  'term1_prob_pretty': term1_prob_pretty,
                  'term2_prob_pretty': term2_prob_pretty,
                  'joint_prob': both_prob_pretty,
                  'independent_joint_prob': independent_prob_pretty,
                  'covariance': covariance_pretty,
                  'ratio': ratio_pretty,
                  'r': r,
                  'term1_upvotes': term1_upvotes,
                  'term2_upvotes': term2_upvotes,
                  'term1_worst_body': term1_worst_body,
                  'r_squared': round(r_squared, 2)}
        form = CorrelationForm(initial={'term1': term1, 'term2': term2})
        return render_to_response('bwog/versus.html', {'res': result, 'form': form}, context_instance=RequestContext(request))


def article_comments(request, article_id):
    try:
        bwog_article = BwogArticle.objects.get(id=article_id)
        bwog_article += 2
    except BwogArticle.DoesNotExist:
        raise Http404
    article_comments = {}
    return render_to_response('bwog/article_comments.html', {'article_comments': article_comments}, context_instance=RequestContext(request))

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


def gram_weight(gram, gram_class):  # only supports up to trigrams at the moment
    if GRAM_CLASS.DOWN == gram_class:
        prefix = 'down:'
    elif GRAM_CLASS.UP == gram_class:
        prefix = 'up:'
    r = redis.Redis()

    weight = r.get(prefix + simplejson.dumps(gram))
    print weight, gram
    if None == weight:
        bigram_one = (gram[0], gram[1])
        bigram_two = (gram[1], gram[2])
        bigram_one_weight = r.get(prefix + simplejson.dumps(bigram_one))
        bigram_two_weight = r.get(prefix + simplejson.dumps(bigram_two))
        print bigram_one_weight, bigram_one
        print bigram_two_weight, bigram_two

        if None == bigram_one_weight:
            print bigram_one
            bg_one_first = r.get(prefix + simplejson.dumps(prefix + bigram_one[0]))
            bg_one_second = r.get(prefix + simplejson.dumps(prefix + bigram_one[1]))
            if None == bg_one_first:
                bg_one_first = 0.0
            else:
                bg_one_first = float(bg_one_first)
            if None == bg_one_second:
                bg_one_second = 0.0
            else:
                bg_one_second = float(bg_one_second)
            bigram_one_weight = bg_one_first / 2 + bg_one_second / 2
        else:
            bigram_one_weight = float(bigram_one_weight)

        if None == bigram_two_weight:
            bg_two_first = r.get(prefix + simplejson.dumps(prefix + bigram_two[0]))
            bg_two_second = r.get(prefix + simplejson.dumps(prefix + bigram_two[1]))
            if None == bg_two_first:
                bg_two_first = 0.0
            else:
                bg_two_first = float(bg_two_first)
            if None == bg_two_second:
                bg_two_second = 0.0
            else:
                bg_two_second = float(bg_two_second)
            bigram_two_weight = bg_two_first / 2 + bg_two_second / 2
        else:
            bigram_two_weight = float(bigram_two_weight)

        weight = bigram_one_weight / 2 + bigram_two_weight / 2
    else:
        weight = float(weight)
    return weight


def get_ranked_hash(ranked, val_function):
    ranked_comments = [
        {'rank': i + 1,
            'ranked_value': val_function(ranked[i]),
            'author': ranked[i].author,
            'bwog_id': ranked[i].bwog_id,
            'body': ranked[i].body,
            'article_id': ranked[i].article_id,
            'article': ranked[i].article}
        for i in range(0, len(ranked) - 1)
    ]
    return ranked_comments
