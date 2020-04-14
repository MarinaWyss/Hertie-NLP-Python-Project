# coding: utf-8

import pandas as pd
from Data_Prep import DataPrep

def test_full_data():
    # instatiate
    res = DataPrep().full_data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'article_text', 'article_title', 'date', 'link', 'publisher'}
    assert res.shape[0] > 9000
    assert set(res.publisher) == {'nbc', 'politico', 'AP', 'new_york_times',
                                  'buzzfeed', 'washington_times', 'Fox', 'Breitbart'}

def test_article_data():
    # instantiate
    res = DataPrep().article_data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'article_text', 'article_title', 'date', 'link', 'publisher',
                                'Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg', 'Bloomberg',
                                'Klobuchar', 'Yang', 'Steyer', 'Gabbard', 'candidates_mentioned'}
    assert res.shape[0] > 6000
    assert all(res.candidates_mentioned >= 1)

def test_sentence_data():
    # instatiate
    res = DataPrep().sentence_data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'Bloomberg', 'Trump', 'link', 'article_text', 'Sanders', 'candidates_mentioned',
                                'article_id', 'Yang', 'Warren', 'Steyer', 'date', 'Klobuchar', 'Buttigieg', 'Gabbard',
                                'publisher', 'article_title', 'Biden'}
    assert res.shape[0] > 50000
    assert all(res.candidates_mentioned >= 1)

