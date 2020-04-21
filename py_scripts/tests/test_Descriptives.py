# coding: utf-8

import pandas as pd
from Descriptives import Descriptives

def test_total_candidate_mentions():
    # instantiate
    res = Descriptives().total_candidate_mentions()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape == (10, 2)
    assert set(res['candidate']) == {'Warren', 'Trump', 'Gabbard', 'Biden', 'Yang', 'Steyer',
                                      'Klobuchar', 'Sanders', 'Buttigieg', 'Bloomberg'}
    assert all(res['count'] >= 90)

def test_mentions_over_time():
    # instatiate
    res = Descriptives().mentions_over_time()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert res.shape[0] >= 300
    assert res.shape[1] == 3
    assert set(res['candidates']) == {'Warren', 'Trump', 'Gabbard', 'Biden', 'Yang', 'Steyer',
                                      'Klobuchar', 'Sanders', 'Buttigieg', 'Bloomberg'}




