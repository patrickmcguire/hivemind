#!/usr/bin/python
import numpy
from django.core.management.base import BaseCommand
from main.models import BwogComment
import scipy
import redis
import simplejson
from stats import NgramCount
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):
        ngram_size = int(args[0])
        damp = int(args[1])
        models = BwogComment.objects.all()
        print len(models)
        ngram_count = NgramCount(models, lambda c: c.body, lambda c: c.id, ngram_size)
        all_grams = ngram_count.all_grams
        A = ngram_count.matrix

        nz = A.nonzero()
        w = csv.writer(open('mat.mat', 'w'))
        for r, c in zip(nz[0], nz[1]):
            w.writerow((r, c, A[r, c]))

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
