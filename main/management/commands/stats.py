#!/usr/bin/python
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from main.models import BwogComment
import nltk
from nltk import ngrams
from nltk import FreqDist
import numpy
import scipy
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import lsqr

class Command(BaseCommand):
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
       
        first_id = min(trigram_counts.keys())
        A = lil_matrix([len(trigram_counts.keys()), len(all_trigrams)])
        for comment_id in trigram_counts.keys():
            m = comment_id - first_id
            comment_trigram_count = trigram_counts[comment_id]
            for trigram_index in comment_trigram_count.keys():
                    trigram_count = comment_trigram_count[trigram_index]
                    n = trigram_index
                    try:
                        A[m,n] = trigram_count
                    except:
                        exit()

        upvates = []
        downvotes = []
        for comment in BwogComment.objects.all():
            upvotes.append([comment.upvotes])
            downvotes.append([comment.downvotes])
        
        upvotes = array(upvotes)
        downvotes = array(downvotes)
        
        upvote_sol = lsqr(A, upvotes, damp=4.0)
        print upvote_sol[0]
        upvote_weights = upvote_sol[0]
        upvote_tuples = []
        for ngram_index in range(0,len(upvote_weights)-1):
            upvote_tuples.append([all_trigrams[ngram_index], upvote_weights[ngram_index]])
        upvote_tuples.sort(key=lambda gram_weight: gram_weight[1])
        upvote_tuples.reverse()
        print "UPVOTES"
        for tup in upvote_tuples:
            print tup

        downvote_sol = lsqr(A, downvotes, damp=4.0)
        print downvote_sol[0]
        downvote_weights = downvote_sol[0]
        downvote_tuples = []
        for ngram_index in range(0, len(downvote_weights) - 1):
            downvote_tuples.append([all_trigrams[ngram_index], upvote_weights[ngram_index]])
        downvote_tuples.sort(key=lambda gram_weight: gram_weight[1])
        downvote_tuples.reverse()
        print "DOWNVOTES"
        for tup in downvote_tuples:
            print tup
