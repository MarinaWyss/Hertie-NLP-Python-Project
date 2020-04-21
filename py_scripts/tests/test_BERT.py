# coding: utf-8

import pandas as pd
import numpy as np
import torch
from string import punctuation
from BERT import BERT

def test_data():
    # instantiate
    res = BERT().data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'article_text', 'label'}
    assert res.shape[0] > 1
    names = ['Biden', 'Sanders', 'Bernie', 'Bernard', 'Joe', 'Senator', 'Vice President']
    assert not res['article_text'].str.contains('|'.join(names)).any()

def test_prepped_data():
    # instantiate
    res = BERT().prepped_data()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'article_text', 'label'}
    assert res.shape[0] > 1
    assert not any(p in res['article_text'] for p in punctuation)

def test_train_test_split():
    # instantiate
    res_train, res_val, res_test = BERT().train_test_split()

    # assertions
    assert res_train.shape == (70, 2)
    assert res_val.shape == (20, 2)
    assert res_test.shape == (10, 2)

def test_bert_model():
    # instantiate
    x_train, x_val, x_test, y_train, y_val, y_test = BERT().bert_model()

    # assertions
    assert isinstance(x_train, torch.Tensor)
    assert all(isinstance(i, torch.Tensor) for i in [x_train, x_val, x_test, y_train, y_val, y_test])
    assert all(i.shape[2] == 768 for i in [x_train, x_val, x_test])
    assert all(set(np.unique(i.round().numpy())) == {0, 1} for i in [y_train, y_val, y_test])
