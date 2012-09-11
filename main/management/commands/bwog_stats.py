#!/usr/bin/python
import numpy
from django.core.management.base import BaseCommand
from main.models import BwogComment
import scipy
from scipy.sparse import lil_matrix
import redis
import simplejson
from stats import NgramCount


class Command(BaseCommand):

    def handle(self, *args, **options):
        ngram_size = int(args[0])
        damp = int(args[1])
        models = BwogComment.objects.all()
        print len(models)
        ngram_count = NgramCount(models, lambda c: c.body, lambda c: c.id, ngram_size)
        gram_counts = ngram_count.counts
        all_grams = ngram_count.all_grams

        first_id = min(gram_counts.keys())
        A = lil_matrix((len(gram_counts.keys()), len(all_grams)))
        print A.shape
        for comment_id in gram_counts.keys():
            m = comment_id - first_id
            comment_gram_count = gram_counts[comment_id]
            for gram_index in comment_gram_count.keys():
                    gram_count = comment_gram_count[gram_index]
                    n = gram_index
                    try:
                        A[m, n] = gram_count
                    except:
                        print m
                        print n
                        exit()

        upvotes = []
        downvotes = []
        for comment in models:
            upvotes.append([comment.upvotes])
            downvotes.append([comment.downvotes])

        upvotes = numpy.array(upvotes)
        downvotes = numpy.array(downvotes)

        A = A.tocsr()
        upvote_weights = scipy.sparse.linalg.lsqr(A, upvotes, damp=damp)[0]
        upvote_tuples = []
        for ngram_index in range(0, len(upvote_weights) - 1):
            upvote_tuples.append([all_grams[ngram_index], upvote_weights[ngram_index]])

        downvote_weights = scipy.sparse.linalg.lsqr(A, downvotes, damp=damp)[0]
        downvote_tuples = []
        for ngram_index in range(0, len(downvote_weights) - 1):
            downvote_tuples.append([all_grams[ngram_index], downvote_weights[ngram_index]])

        r = redis.Redis()
        for tup in upvote_tuples:
            r.set('up:' + simplejson.dumps(tup[0]), tup[1])

        for tup in downvote_tuples:
            r.set('down:' + simplejson.dumps(tup[0]), tup[1])
