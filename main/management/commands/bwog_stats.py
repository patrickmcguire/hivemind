#!/usr/bin/python
import numpy
from django.core.management.base import BaseCommand
from main.models import BwogComment
import nltk
from nltk import ngrams
import scipy
from scipy.sparse import *
from scipy.sparse.linalg import *
import redis
import simplejson


class Command(BaseCommand):

    def handle(self, *args, **options):
        damp = int(args[0])
        all_trigrams = []
        trigram_indices = {}
        for comment in BwogComment.objects.all():
            body = comment.body
            words = nltk.word_tokenize(body)
            trigrams = ngrams(words, 3)
            for trigram in trigrams:
                if not trigram in trigram_indices:
                    all_trigrams.append(trigram)
                    trigram_indices[trigram] = len(all_trigrams) - 1

        print len(trigram_indices.keys())
        trigram_counts = {}
        for comment in BwogComment.objects.all():
            body = comment.body
            words = nltk.word_tokenize(body)
            trigrams = ngrams(words, 3)
            this_count = {}
            for trigram in trigrams:
                trigram_index = trigram_indices[trigram]
                if not trigram_index in this_count:
                    this_count[trigram_index] = 1
                else:
                    this_count[trigram_index] += 1
            trigram_counts[comment.id] = this_count

        print len(trigram_counts.keys())
        print len(all_trigrams)
        first_id = min(trigram_counts.keys())
        A = lil_matrix((len(trigram_counts.keys()), len(all_trigrams)))
        print A.shape
        for comment_id in trigram_counts.keys():
            m = comment_id - first_id
            comment_trigram_count = trigram_counts[comment_id]
            for trigram_index in comment_trigram_count.keys():
                    trigram_count = comment_trigram_count[trigram_index]
                    n = trigram_index
                    try:
                        A[m, n] = trigram_count
                    except:
                        print m
                        print n
                        exit()

        upvotes = []
        downvotes = []
        for comment in BwogComment.objects.all():
            upvotes.append([comment.upvotes])
            downvotes.append([comment.downvotes])

        upvotes = numpy.array(upvotes)
        downvotes = numpy.array(downvotes)

        A = A.tocsr()
        upvote_weights = scipy.sparse.linalg.lsqr(A, upvotes, damp=damp)[0]
        upvote_tuples = []
        for ngram_index in range(0, len(upvote_weights) - 1):
            upvote_tuples.append([all_trigrams[ngram_index], upvote_weights[ngram_index]])

        downvote_weights = scipy.sparse.linalg.lsqr(A, downvotes, damp=damp)[0]
        downvote_tuples = []
        for ngram_index in range(0, len(downvote_weights) - 1):
            downvote_tuples.append([all_trigrams[ngram_index], downvote_weights[ngram_index]])

        r = redis.Redis()
        for tup in upvote_tuples:
            r.set('up:' + simplejson.dumps(tup[0]), tup[1])

        for tup in downvote_tuples:
            r.set('down:' + simplejson.dumps(tup[0]), tup[1])
