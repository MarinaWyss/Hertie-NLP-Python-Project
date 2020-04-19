# coding: utf-8

import pandas as pd
from Sentiment_Analysis import SentimentAnalysis

def test_sentence_data():
    # instantiate
    res = SentimentAnalysis().sentence_data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape[0] >= 140000
    assert res.shape[1] == 18
    assert all(res.candidates_mentioned >= 1)
    assert set(res.publisher) == {'nbc', 'politico', 'AP', 'new_york_times',
                                  'buzzfeed', 'washington_times', 'Fox', 'Breitbart'}

def test_sentiment_data():
    # instantiate
    res = SentimentAnalysis().sentiment_data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape[0] >= 140000
    assert res.shape[1] == 19
    assert 'sentiment' in set(res.columns)
    assert all(res.candidates_mentioned >= 1)
    assert set(res.publisher) == {'nbc', 'politico', 'AP', 'new_york_times',
                                  'buzzfeed', 'washington_times', 'Fox', 'Breitbart'}

def test_outlet_sentiment():
    # instantiate
    res = SentimentAnalysis().outlet_sentiment()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape == (5, 8)
    assert set(res.columns) == {'AP', 'Breitbart', 'Fox', 'Buzzfeed', 'NBC',
                                'New York Times', 'Politico', 'Washington Times'}

def test_sentiment_candidate_outlet():
    # instantiate
    res = SentimentAnalysis().sentiment_candidate_outlet()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape == (8, 4)
    assert set(res.publisher) == {'nbc', 'politico', 'AP', 'new_york_times',
                                  'buzzfeed', 'washington_times', 'Fox', 'Breitbart'}
    assert set(res.columns) == {'publisher', 'trump_mean', 'sanders_mean', 'biden_mean'}

def test_sentiment_time():
    # instantiate
    res = SentimentAnalysis().sentiment_time()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape[0] >= 300
    assert set(res.columns) == {'date', 'candidate', 'sentiment'}
    assert ({'yang', 'trump', 'sanders', 'buttigieg', 'steyer', 'warren',
            'bloomberg', 'klobuchar', 'biden', 'gabbard'}).issubset(set(res.candidate))
