#!/usr/bin/python
import numpy
from django.core.management.base import BaseCommand
from main.models import BwogComment
import nltk
from nltk import ngrams
from scipy.sparse import *
from scipy.linalg import inv
from scipy.sparse.linalg import *
import pickle


class Command(BaseCommand):

    def _sparse_transpose(self, m):
        shape = m.shape
        m2 = lil_matrix(shape[1], shape[0])
        for i in range(0, len(shape[0])):
            for j in range(0, len(shape[1])):
                if 0 != m[i, j]:
                    m2[j, i] = m[i, j]
        return m2.tocsr

    def handle(self, *app_labels, **options):
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
        print A.shape
        tran = A.transpose().tocsr()
        print tran.shape
        sq = tran.tocsr() * A
        print sq.shape
        sq_inv = inv(sq)
        p = sq_inv * tran
        upvote_tuples = []
        for ngram_index in range(0, len(upvote_weights) - 1):
            upvote_tuples.append([all_trigrams[ngram_index], upvote_weights[ngram_index]])
        upvote_tuples.sort(key=lambda gram_weight: gram_weight[1])
        upvote_tuples.reverse()

        pickle.dump(upvote_tuples, file("upvotes.weight", 'w'))

        downvote_sol = p * downvotes

        downvote_weights = downvote_sol[0]
        downvote_tuples = []
        for ngram_index in range(0, len(downvote_weights) - 1):
            downvote_tuples.append([all_trigrams[ngram_index], downvote_weights[ngram_index]])
        downvote_tuples.sort(key=lambda gram_weight: gram_weight[1])
        downvote_tuples.reverse()
        pickle.dump(downvote_tuples, file("downvotes.weight", 'w'))
