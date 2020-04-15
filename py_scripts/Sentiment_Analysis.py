# coding: utf-8

import pandas as pd
from nltk.corpus import stopwords
import re
import numpy as np
from textblob import TextBlob
import warnings


class SentimentAnalysis:
    """
    A class to runs a TextBlob sentiment analysis and create descriptive plots.
    """
    def __init__(self):
        self.path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/'
        self.candidates = ['Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg',
                           'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard']
        self._sentence_data = None
        self._sentiment_data = None

    def sentence_data(self):
        """
        Reads in sentence data from scraper.
        return: pd.DataFrame
        """
        data = pd.read_csv(self.path + 'data/sentence_data.csv')

        # setup
        sentences = data['article_text']

        # lowercase everything
        sentences = [sentences.lower() for sentences in sentences]

        # remove punctuation
        sentences = [s.replace("’s",'') for s in sentences] # remove apostrophe s first
        sentences = [re.sub(r'[^\w\s]','',s) for s in sentences]

        # remove numbers
        sentences = [re.sub('[0-9]','', s) for s in sentences]

        # remove double space
        sentences = [s.replace("  ",' ') for s in sentences]

        # remove stopwords
        clean = []
        for item in sentences:
            for word in stopwords.words('english'):
                item = item.replace(" " + word + " ", ' ')
            clean.append(item)

        data['article_text_clean'] = clean

        self._sentence_data = data
        
        return self._sentence_data


    def sentiment_data(self):
        """
        Uses TextBlob's rule-based API to conduct sentiment analysis. Adds score to new column in data.
        return: pd.DataFrame
        """
        # setup
        data = self.sentence_data()

        text = data['article_text_clean']
        score = []
        
        for sentence in text:
            sentence = TextBlob(sentence)
            x = sentence.sentiment.polarity
            score.append(x)

        data['score'] = score

        # Convert float score to category based on binning to get 5 levels
        data['sentiment'] = pd.cut(data['score'],
                            bins=5,
                            labels=[1, 2, 3, 4, 5])
        data['sentiment'] = pd.to_numeric(data['sentiment'])

        sentiment_data = data.drop('score', axis=1)

        self._sentiment_data = sentiment_data

        return self._sentiment_data


    def outlet_sentiment(self):
        """
        Calculates the sentiment score breakdown as a percent per outlet.
        return: pd.DataFrame
        """
        data = self.sentiment_data()

        # AP sentiment
        AP = data.loc[data['publisher'] == "AP"]
        AP_sent = AP['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        AP_sent_count = AP_sent.value_counts().sort_index()
        # get percent per sentiment category
        AP_1 = AP_sent_count[1]/len(AP_sent)
        AP_2 = AP_sent_count[2]/len(AP_sent)
        AP_3 = AP_sent_count[3]/len(AP_sent)
        AP_4 = AP_sent_count[4]/len(AP_sent)
        AP_5 = AP_sent_count[5]/len(AP_sent)

        # Breitbart sentiment
        Breitbart = data.loc[data['publisher'] == "Breitbart"]
        Breitbart_sent = Breitbart['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        Breitbart_sent_count = Breitbart_sent.value_counts().sort_index()
        # get percent per sentiment category
        Breitbart_1 = Breitbart_sent_count[1]/len(Breitbart_sent)
        Breitbart_2 = Breitbart_sent_count[2]/len(Breitbart_sent)
        Breitbart_3 = Breitbart_sent_count[3]/len(Breitbart_sent)
        Breitbart_4 = Breitbart_sent_count[4]/len(Breitbart_sent)
        Breitbart_5 = Breitbart_sent_count[5]/len(Breitbart_sent)

        # Fox sentiment
        Fox = data.loc[data['publisher'] == "Fox"]
        Fox_sent = Fox['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        Fox_sent_count = Fox_sent.value_counts().sort_index()
        # get percent per sentiment category
        Fox_1 = Fox_sent_count[1]/len(Fox_sent)
        Fox_2 = Fox_sent_count[2]/len(Fox_sent)
        Fox_3 = Fox_sent_count[3]/len(Fox_sent)
        Fox_4 = Fox_sent_count[4]/len(Fox_sent)
        Fox_5 = Fox_sent_count[5]/len(Fox_sent)

        # Buzzfeed sentiment
        buzzfeed = data.loc[data['publisher'] == "buzzfeed"]
        buzzfeed_sent = buzzfeed['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        buzzfeed_sent_count = buzzfeed_sent.value_counts().sort_index()
        # get percent per sentiment category
        buzzfeed_1 = buzzfeed_sent_count[1]/len(buzzfeed_sent)
        buzzfeed_2 = buzzfeed_sent_count[2]/len(buzzfeed_sent)
        buzzfeed_3 = buzzfeed_sent_count[3]/len(buzzfeed_sent)
        buzzfeed_4 = buzzfeed_sent_count[4]/len(buzzfeed_sent)
        buzzfeed_5 = buzzfeed_sent_count[5]/len(buzzfeed_sent)

        # NBC
        nbc = data.loc[data['publisher'] == "nbc"]
        nbc_sent = nbc['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        nbc_sent_count = nbc_sent.value_counts().sort_index()
        # get percent per sentiment category
        nbc_1 = nbc_sent_count[1]/len(nbc_sent)
        nbc_2 = nbc_sent_count[2]/len(nbc_sent)
        nbc_3 = nbc_sent_count[3]/len(nbc_sent)
        nbc_4 = nbc_sent_count[4]/len(nbc_sent)
        nbc_5 = nbc_sent_count[5]/len(nbc_sent)

        # New York Times
        new_york_times = data.loc[data['publisher'] == "new_york_times"]
        new_york_times_sent = new_york_times['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        new_york_times_sent_count = new_york_times_sent.value_counts().sort_index()
        # get percent per sentiment category
        new_york_times_1 = new_york_times_sent_count[1]/len(new_york_times_sent)
        new_york_times_2 = new_york_times_sent_count[2]/len(new_york_times_sent)
        new_york_times_3 = new_york_times_sent_count[3]/len(new_york_times_sent)
        new_york_times_4 = new_york_times_sent_count[4]/len(new_york_times_sent)
        new_york_times_5 = new_york_times_sent_count[5]/len(new_york_times_sent)

        # Politico
        politico = data.loc[data['publisher'] == "politico"]
        politico_sent = politico['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        politico_sent_count = politico_sent.value_counts().sort_index()
        # get percent per sentiment category
        politico_1 = politico_sent_count[1]/len(politico_sent)
        politico_2 = politico_sent_count[2]/len(politico_sent)
        politico_3 = politico_sent_count[3]/len(politico_sent)
        politico_4 = politico_sent_count[4]/len(politico_sent)
        politico_5 = politico_sent_count[5]/len(politico_sent)

        # Washington Times
        washington_times = data.loc[data['publisher'] == "washington_times"]
        washington_times_sent = washington_times['sentiment'].sort_values(ascending=True)
        # get sentiment counts
        washington_times_sent_count = washington_times_sent.value_counts().sort_index()
        # get percent per sentiment category
        washington_times_1 = washington_times_sent_count[1]/len(washington_times_sent)
        washington_times_2 = washington_times_sent_count[2]/len(washington_times_sent)
        washington_times_3 = washington_times_sent_count[3]/len(washington_times_sent)
        washington_times_4 = washington_times_sent_count[4]/len(washington_times_sent)
        washington_times_5 = washington_times_sent_count[5]/len(washington_times_sent)

        publishers = pd.DataFrame({
            'AP': [AP_1, AP_2, AP_3, AP_4, AP_5],
            'Breitbart': [Breitbart_1, Breitbart_2, Breitbart_3, Breitbart_4, Breitbart_5],
            'Fox': [Fox_1, Fox_2, Fox_3, Fox_4, Fox_5],
            'Buzzfeed': [buzzfeed_1, buzzfeed_2, buzzfeed_3, buzzfeed_4, buzzfeed_5],
            'NBC': [nbc_1, nbc_2, nbc_3, nbc_4, nbc_5],
            'New York Times': [new_york_times_1, new_york_times_2, new_york_times_3, new_york_times_4, new_york_times_5],
            'Politico': [politico_1, politico_2, politico_3, politico_4, politico_5],
            'Washington Times': [washington_times_1, washington_times_2, washington_times_3, washington_times_4, washington_times_5]
        })

        return publishers


    def sentiment_candidate_outlet(self):
        """
        Calculates the sentiment averages per candidate and outlet.
        return: pd.DataFrame
        """
        data = self.sentiment_data()

        trump = data.loc[data['Trump'] == 1]
        trump_sentiment = trump.groupby('publisher')['sentiment'].mean().reset_index()

        sanders = data.loc[data['Sanders'] == 1]
        sanders_sentiment = sanders.groupby('publisher')['sentiment'].mean().reset_index()

        biden = data.loc[data['Biden'] == 1]
        biden_sentiment = biden.groupby('publisher')['sentiment'].mean().reset_index()

        sentiment_candidate_outlet = trump_sentiment.merge(sanders_sentiment, on = "publisher", how = "left")
        sentiment_candidate_outlet = sentiment_candidate_outlet.merge(biden_sentiment, on = "publisher", how = "left")
        sentiment_candidate_outlet.columns = ['publisher', 'trump_mean', 'sanders_mean', 'biden_mean']

        return sentiment_candidate_outlet


    def sentiment_time(self):
        """
        Calculates the mean sentiment score per candidate per day.
        return: pd.DataFrame
        """
        warnings.simplefilter(action='ignore')

        data = self.sentiment_data()

        # filter sentences only about one candidate
        candidate_sentiment = data.loc[data['candidates_mentioned'] == 1]

        # create new column with candidate name
        candidate_sentiment['candidate'] = candidate_sentiment['article_text'].str.extract('({})'.format('|'.join(self.candidates)),
                                            flags = re.IGNORECASE, expand = False).str.lower().fillna('')
        candidate_sentiment['candidate'] = np.where(candidate_sentiment['article_text'].str.contains('bernie'), 'sanders', candidate_sentiment['candidate'])
        candidate_sentiment = candidate_sentiment[['date', 'sentiment', 'candidate']]

        # make dates consistent and filter for time frame
        candidate_sentiment['date'] = pd.to_datetime(candidate_sentiment['date'], errors='coerce')
        mask = (candidate_sentiment['date'].astype('str') >= "2020-03-01") & (candidate_sentiment['date'].astype('str') < "2020-03-30")
        candidate_sentiment = candidate_sentiment.loc[mask]

        # mean sentiment per day
        mean_per_day = candidate_sentiment.groupby(['date', 'candidate']).mean()
        mean_per_day.reset_index(inplace = True)
        mean_per_day.dropna(inplace = True)

        return mean_per_day



