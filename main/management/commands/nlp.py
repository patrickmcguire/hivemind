from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from main.models import BwogArticle
from main.models import BwogComment
from main.models import ParsedItem
import nltk
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from numpy.linalg import solve, norm
from numpy.random import rand
from nltk import PunktSentenceTokenizer

class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        for article in BwogArticle.objects.all():
            sentence_tokenizer = PunktSentenceTokenizer()
            sentences = sentence_tokenizer.tokenize(article.body)
            for sentence_index in range(len(sentences)):
                sentence = sentences[sentence_index]
                sentence_words = nltk.word_tokenize(sentence)
                tagged = nltk.pos_tag(sentence_words)
                for tup_index in range(len(tagged)):
                    tup = tagged[tup_index]
                    article_word = tup[0]
                    article_tag = tup[1]
                    p = ParsedItem(content_object=article, word=article_word, tag=article_tag,
                                   sentence_sequence=sentence_index, word_sequence=tup_index)
                    p.save()
                    print p
