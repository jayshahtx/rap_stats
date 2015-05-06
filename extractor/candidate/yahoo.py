# -*- coding: utf-8 -*-
"""Generates key terms using Yahoo's content analysis API"""
import logging
import yql


def generate_key_terms(raw_text):
    """Generates key terms using Yahoo's term extractor"""
    y = yql.Public()
    query = 'select * from contentanalysis.analyze where text=@text'

    try:
        result = y.execute(query, {'text': raw_text})

        try:
            key_terms = [result.results['entities']['entity']['text']['content']]
        except:
            key_terms = [
                x['text']['content'] for x in result.results['entities']['entity']
            ]
        return key_terms
    except:
        print 'yql failed to execute.'
        return []

