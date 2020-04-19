# coding: utf-8

import pandas as pd
import numpy as np
from dateutil.parser import parse
import warnings

warnings.simplefilter(action='ignore')


class DataPrep:
    """
    Creates two merged datasets: one articles with articles about candidates 
    and one with sentences about candidates, from eight scraped sources.
    """
    def __init__(self):
        self.candidates = ['Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg', 
                           'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard']
        self.path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/'
        self._full_data = None
        self._article_data = None
        self._sentence_data = None

    def full_data(self):
        """
        Merges data set of articles scraped from eight different U.S. media outlets
        return: pd.DataFrame
        """
        # load all data sets
        breitbart = pd.read_csv(self.path + 'data/breitbart_data.csv')
        fox = pd.read_csv(self.path + 'data/fox_data.csv')
        wt = pd.read_csv(self.path + 'data/wt_data.csv')
        ap = pd.read_csv(self.path + 'data/ap_data.csv')
        nbc = pd.read_csv(self.path + 'data/nbc_data.csv')
        nyt = pd.read_csv(self.path + 'data/nyt_data.csv')
        politico = pd.read_csv(self.path + 'data/politico_data.csv')
        buzzfeed = pd.read_csv(self.path + 'data/buzzfeed_data.csv')
        
        # make dates comparable
        fox['date'] = [x.split('T')[0] for x in fox['date']]
        wt['date'] = [x.replace(' -\n\t\t\t\n\t\t\t\tAssociated Press\n -    Updated:', '') for x in wt['date']]
        wt['date'] = [x.replace(' -\n\t\t\t\n\t\t\t\tThe Washington Times\n -    Updated:', '') for x in wt['date']]
        wt['date'] = [parse(x) for x in wt['date']]
        ap['date'] = [x.split('T')[0] for x in ap['date']]
        nbc = nbc.copy().dropna()
        nbc['date'] = [parse(x) for x in nbc['date']]
        buzzfeed['date'] = [x.replace('Posted on ', '').replace('Last updated on ', '') for x in buzzfeed['date']]
        buzzfeed['date'] = [x.strip() for x in buzzfeed['date']]
        buzzfeed['date'] = [x.split(',')[0:2] for x in buzzfeed['date']]
        buzzfeed['date'] = [''.join(x) for x in buzzfeed['date']]
        buzzfeed['date'] = [parse(x) for x in buzzfeed['date']]
        
        # merge
        self._full_data = pd.concat([
            breitbart,
            fox,
            wt,
            ap,
            nbc,
            nyt,
            politico,
            buzzfeed
        ])
        
        return self._full_data
    
    def article_data(self):
        """
        Creates new columns on the full_data noting whether a candidate was mentioned,
        and how many were mentioned in each article.
        return: pd.DataFrame
        """
        article_data = self.full_data()

        # identify candidates 
        article_data['Trump'] = pd.np.where(article_data['article_text'].str.contains('Trump'), 1, 0)
        article_data['Sanders'] = pd.np.where(article_data['article_text'].str.contains('Bernie'), 1, 
                                              (np.where(article_data['article_text'].str.contains('Sanders'), 1, 0)))
        article_data['Biden'] = pd.np.where(article_data['article_text'].str.contains('Biden'), 1, 0)
        article_data['Warren'] = pd.np.where(article_data['article_text'].str.contains('Warren'), 1, 0)
        article_data['Buttigieg'] = pd.np.where(article_data['article_text'].str.contains('Buttigieg'), 1, 0)
        article_data['Bloomberg'] = pd.np.where(article_data['article_text'].str.contains('Bloomberg'), 1, 0)
        article_data['Klobuchar'] = pd.np.where(article_data['article_text'].str.contains('Klobuchar'), 1, 0)
        article_data['Yang'] = pd.np.where(article_data['article_text'].str.contains('Yang'), 1, 0)
        article_data['Steyer'] = pd.np.where(article_data['article_text'].str.contains('Steyer'), 1, 0)
        article_data['Gabbard'] = pd.np.where(article_data['article_text'].str.contains('Gabbard'), 1, 0)
        
        # limit to only articles where candidate is mentioned
        article_data['candidates_mentioned'] = article_data[self.candidates].sum(axis = 1)
        article_data = article_data[article_data['candidates_mentioned'] != 0]
       
        self._article_data = article_data
            
        return self._article_data
    
    def save_article_data(self):
        """
        Saves article data.
        """
        # read in old data
        old_data = pd.read_csv(self.path + 'data/article_data.csv')
        num_old = len(old_data)

        # append new data
        article_data = old_data.append(self.article_data()).drop_duplicates()
        
        # save new .csv
        article_data.to_csv(self.path + "data/article_data.csv", index = False)
        num_now = len(article_data)

        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        print("difference: {}".format(num_now - num_old))

    def sentence_data(self):
        """
        Breaks the full_data into sentences, and creates new columns noting whether 
        a candidate was mentioned, and how many were mentioned in each sentence.
        return: pd.DataFrame
        """
        sentence_data = self.full_data()

        # articles to sentences
        # create article id #
        data_for_sentences = sentence_data[['article_text', 'article_title', 'date', 'link', 'publisher']].copy()
        data_for_sentences = data_for_sentences.reset_index()
        data_for_sentences = data_for_sentences.reset_index().rename(columns = {'level_0': 'article_id'}).drop(columns = 'index')
        
        # split article text to sentences
        sentences = data_for_sentences['article_text'].copy().str.split('.').apply(pd.Series, 1).stack()

        # add correct article id # to each sentence
        sentences.index.droplevel(-1) 
        sentences.name = 'article_text'
        sentences = sentences.reset_index().drop(columns = 'level_1').rename(columns = {'level_0': 'article_id'})
        
        # drop original article text
        data_for_sentences = data_for_sentences.drop(columns = 'article_text')
        
        # merge sentence article text
        sentence_data = data_for_sentences.merge(sentences, how='left', on='article_id')
        
        # clean up
        mask = sentence_data['article_text'].astype(str).str.len() < 15
        sentence_data.loc[mask, 'article_text'] = ''
        sentence_data = sentence_data[(sentence_data['article_text'] != '')]
        
        # identify candidates 
        sentence_data['Trump'] = pd.np.where(sentence_data['article_text'].str.contains('Trump'), 1, 0)
        sentence_data['Sanders'] = pd.np.where(sentence_data['article_text'].str.contains('Bernie'), 1, 
                                              (np.where(sentence_data['article_text'].str.contains('Sanders'), 1, 0)))
        sentence_data['Biden'] = pd.np.where(sentence_data['article_text'].str.contains('Biden'), 1, 0)
        sentence_data['Warren'] = pd.np.where(sentence_data['article_text'].str.contains('Warren'), 1, 0)
        sentence_data['Buttigieg'] = pd.np.where(sentence_data['article_text'].str.contains('Buttigieg'), 1, 0)
        sentence_data['Bloomberg'] = pd.np.where(sentence_data['article_text'].str.contains('Bloomberg'), 1, 0)
        sentence_data['Klobuchar'] = pd.np.where(sentence_data['article_text'].str.contains('Klobuchar'), 1, 0)
        sentence_data['Yang'] = pd.np.where(sentence_data['article_text'].str.contains('Yang'), 1, 0)
        sentence_data['Steyer'] = pd.np.where(sentence_data['article_text'].str.contains('Steyer'), 1, 0)
        sentence_data['Gabbard'] = pd.np.where(sentence_data['article_text'].str.contains('Gabbard'), 1, 0)
        
        # limit to only articles where candidate is mentioned
        sentence_data['candidates_mentioned'] = sentence_data[self.candidates].sum(axis = 1)
        sentence_data = sentence_data[sentence_data['candidates_mentioned'] != 0]
       
        self._sentence_data = sentence_data
            
        return self._sentence_data
    
    def save_sentence_data(self):
        """
        Saves sentence data.
        """
        # read in old data
        old_data = pd.read_csv(self.path + 'data/sentence_data.csv')
        num_old = len(old_data)

        # append new data
        sentence_data = old_data.append(self.sentence_data()).drop_duplicates()
        
        # save new .csv
        sentence_data.to_csv(self.path + "data/sentence_data.csv", index = False)
        num_now = len(sentence_data)

        print("number of entries in old data: {}".format(num_old))
        print("total number of entries in new data: {}".format(num_now))
        print("difference: {}".format(num_now - num_old))

