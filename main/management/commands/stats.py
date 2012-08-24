import nltk
from nltk import ngrams


class NgramCount:

    def __init__(self, models, text_extractor, id_extractor, size):
        all_grams = []
        gram_indices = {}
        for model in models:
            text = text_extractor(model)
            words = nltk.word_tokenize(text)
            grams = ngrams(words, size)
            for gram in grams:
                if not gram in gram_indices:
                    all_grams.append(gram)
                    gram_indices[gram] = len(all_grams) - 1

        gram_counts = {}
        for model in models:
            text = text_extractor(model)
            words = nltk.word_tokenize(text)
            grams = ngrams(words, size)
            this_count = {}
            for gram in grams:
                gram_index = gram_indices[gram]
                if not gram_index in this_count:
                    this_count[gram_index] = 1
                else:
                    this_count[gram_index] += 1
            gram_counts[id_extractor(model)] = this_count
        self.counts = gram_counts
        self.all_grams = all_grams
        self.gram_indices = gram_indices
