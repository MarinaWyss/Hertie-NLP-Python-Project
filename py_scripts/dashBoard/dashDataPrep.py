import pandas as pd
import numpy as np
import re

from textblob import TextBlob

class DashData:
    def __init__(self):
        self.data = pd.read_csv('/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/data/sentence_data.csv')

    def sentence_data(self):

        sentence_data = self.data

        # convert date to datetime
        sentence_data['date'] = pd.to_datetime(sentence_data['date'], errors='coerce')
        sentence_data['date'] = sentence_data['date'].dt.date

        # filtering weird dates
        mask = sentence_data['date'].astype('str') >= "2020-03-01"
        sentence_data = sentence_data.loc[mask]

        # re-naming publishers
        sentence_data['publisher'] = sentence_data['publisher'].replace({'washington_times': 'WashingtonTimes',
                                                                         'nbc': 'NBC',
                                                                         'new_york_times': 'NewYorkTimes',
                                                                         'politico': 'Politico',
                                                                         'buzzfeed': 'Buzzfeed'})

        return sentence_data

    def mentions_per_day(self):

        sentence_data = self.sentence_data()

        time_data = sentence_data.loc[:, ['date', 'Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg',
                                          'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard']]

        sum_cand_day = time_data.groupby(['date']).sum()
        sum_cand_day.reset_index(inplace=True)

        mentions_over_time = pd.melt(sum_cand_day,
                                     id_vars=['date'],
                                     var_name='candidates',
                                     value_name='count')

        return mentions_over_time

    def mentions_day_publisher(self):

        sentence_data = self.sentence_data()

        time_data_pub = sentence_data.loc[:, ['date', 'publisher', 'Trump', 'Sanders', 'Biden', 'Warren',
                                              'Buttigieg', 'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard']]

        sum_cand_day_pub = time_data_pub.groupby(['date', 'publisher']).sum()
        sum_cand_day_pub.reset_index(inplace=True)

        mentions_over_time_pub = pd.melt(sum_cand_day_pub,
                                         id_vars=['date', 'publisher'],
                                         var_name='candidate',
                                         value_name='count')

        return mentions_over_time_pub

    def sentiment_data(self):

        sentence_data = self.sentence_data()

        # clean up
        sentences = sentence_data['article_text']
        sentences = [sentences.lower() for sentences in sentences]
        sentences = [s.replace("’s", '') for s in sentences]
        sentences = [re.sub(r'[^\w\s]', '', s) for s in sentences]
        sentences = [re.sub('[0-9]', '', s) for s in sentences]
        sentences = [s.replace("  ", ' ') for s in sentences]

        sentence_data['article_text_clean'] = sentences

        # sentiment per sentence
        text = sentence_data['article_text_clean']
        score = []

        for sentence in text:
            sentence = TextBlob(sentence)
            x = sentence.sentiment.polarity
            score.append(x)

        sentence_data['sentiment'] = score

        sentiment_data = sentence_data.loc[sentence_data['candidates_mentioned'] == 1]

        # create new column with candidate name
        sentiment_data['candidate'] = sentiment_data['article_text'].str.extract(
            '({})'.format('|'.join(['Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg',
                                    'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard'])),
            flags=re.IGNORECASE, expand=False).str.lower().fillna('')
        sentiment_data['candidate'] = np.where(sentiment_data['article_text'].str.contains('bernie'),
                                                    'sanders', sentiment_data['candidate'])

        return sentiment_data

    def sentiment_per_day(self):
        cand_sentiment = self.sentiment_data()
        cand_sentiment = cand_sentiment[['date', 'sentiment', 'candidate']]

        sentiment_per_day = cand_sentiment.groupby(['date', 'candidate']).mean()
        sentiment_per_day.reset_index(inplace=True)

        return sentiment_per_day

    def sentiment_day_publisher(self):
        cand_sentiment = self.sentiment_data()
        cand_sentiment = cand_sentiment[['date', 'sentiment', 'publisher', 'candidate']]

        sentiment_day_publisher = cand_sentiment.groupby(['date', 'publisher', 'candidate']).mean()
        sentiment_day_publisher.reset_index(inplace=True)

        return sentiment_day_publisher

