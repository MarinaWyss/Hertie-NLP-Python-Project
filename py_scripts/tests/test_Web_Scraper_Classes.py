# coding: utf-8

import pandas as pd
from Web_Scraper_Classes import WebScraper


def test_scrape_breitbart():
    # instantiate
    res = WebScraper.scrape_breitbart()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "Breitbart")
    assert res.shape == (30, 5)

def test_scrape_fox():
    # instantiate
    res = WebScraper.scrape_fox()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "Fox")
    assert res.shape[0] >= 25

def test_scrape_wt():
    # instantiate
    res = WebScraper.scrape_wt()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "Washington Times")
    assert res.shape[0] >= 25

def test_scrape_ap():
    # instantiate
    res = WebScraper.scrape_ap()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "AP")
    assert res.shape[0] >= 25

def test_scrape_nbc():
    # instantiate
    res = WebScraper.scrape_nbc()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "nbc")
    assert res.shape[0] >= 25

def test_scrape_nyt():
    # instantiate
    res = WebScraper.scrape_nbc()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "new_york_times")
    assert res.shape[0] >= 1

def test_scrape_politico():
    # instantiate
    res = WebScraper.scrape_politico()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "politico")
    assert res.shape[0] >= 25

def test_scrape_buzzfeed():
    # instantiate
    res = WebScraper.scrape_buzzfeed()

    # assertions
    assert isinstance(res, pd.DataFrame)
    assert set(res.columns) == {'publisher', 'date', 'link', 'article_title', 'article_text'}
    assert all(res.publisher == "buzzfeed")
    assert res.shape == (30, 5)
