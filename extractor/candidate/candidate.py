# -*- coding: utf-8 -*-
"""Responsible for generating possible candidates from raw data. Specifically,
determining good key terms and phrases relevant to the documents provided
"""
import logging
import pmi
import nltk_chunking
import yahoo
import rake

from tabulate import tabulate
from unidecode import unidecode


def generate_candidates(raw_data):
    """Generates possible candidates across different sources. First generates
    possible candidates for each source of data and then combines them all
    """

    print('### Generating candidates from raw descriptions')
    return generate_candidates_for_source(raw_data)


def clean_candidates(candidates):
    """Takes a candidate and cleans out the results. Removing whitespace and
    duplicates.
    """
    candidates = [unidecode(x) for x in candidates]
    candidates = [x.lower().strip() for x in candidates]
    return list(set(candidates))


def generate_candidates_for_source(source):
    """Generates the candidates for a single source of data"""

    chunking_terms = clean_candidates(
        nltk_chunking.generate_key_terms(
            unidecode(source)
        )
    )[:10]


    # TODO(matthewe|2014-11-22): Maybe something to explore with more
    # data for bigrams, currently a pretty shitty approach
    # pmi.generate_key_terms(s)

    rake_terms = clean_candidates(rake.generate_key_terms(source))[:10]

    yql_terms = clean_candidates(
        yahoo.generate_key_terms(source)
    )[:10]

    print(
        '### Top Term(s):\n\n{0}'.format(
            tabulate(
                {
                    'yql_terms': yql_terms,
                    'chunking_terms': chunking_terms,
                    'rake_terms': rake_terms,
                },
                headers="keys"
            )
        )
    )

    candidates = list(set(chunking_terms + rake_terms + yql_terms))
    return candidates
