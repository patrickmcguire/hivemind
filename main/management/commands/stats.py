import nltk
from nltk import ngrams
from scipy.sparse import lil_matrix


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

        min_id = min(gram_counts.keys())
        min_ngram = 0

        mat = lil_matrix((len(gram_counts.keys()), len(all_grams)))

        for model_id in gram_counts.keys():
            count_dict = gram_counts[model_id]
            for gram_id in count_dict.keys():
                mat[model_id - min_id, gram_id - min_ngram] = count_dict[gram_id]

        self.counts = gram_counts
        self.all_grams = all_grams
        self.gram_indices = gram_indices
        self.matrix = mat.tocsr()
