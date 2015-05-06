# -*- coding: utf-8 -*-
"""Computes the top bigrams as possible candidates for a given document. To do
so this will use PMI and bigrams.
"""
import logging
import nltk
from nltk.collocations import *


bigram_measures = nltk.collocations.BigramAssocMeasures()


def generate_key_terms(raw_text):
    # Read in our data
    finder = BigramCollocationFinder.from_words(
        raw_text.split()
    )

    # Only get bigrams that match criteria
    finder.apply_freq_filter(2)

    # Return the top bigrams
    top_bigrams = finder.nbest(
        bigram_measures.pmi,
        5
    )

    return top_bigrams
