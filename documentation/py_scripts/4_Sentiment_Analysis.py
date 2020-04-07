#!/usr/bin/env python
# coding: utf-8

# # Sentiment Analysis

# **This class pre-processes the data, runs a TextBlob sentiment analysis and creates the plots that are used on an ongoing basis. Many more plots and descriptives can be found in preparatory_scripts/all-descriptives.ipynb**

# In[81]:


import pandas as pd
import nltk
from nltk.tokenize import wordpunct_tokenize
from string import punctuation
from nltk.corpus import stopwords
import re
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from textblob import TextBlob
import warnings


# In[102]:


class SentimentAnalysis:
    """
    A class to runs a TextBlob sentiment analysis and create descriptive plots.
    """
    def sentence_data():
        """
        Reads in sentence data from scraper.
        return: pd.DataFrame
        """
        data = pd.read_csv('data/sentence_data.csv')
        
        return data
    
    def prep_data():
        """
        Removes punctuation, numbers, stopwords and lowercases from sentence data and adds to new column in data.
        return: pd.DataFrame
        """
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
        
        return data
    
    def sentiment_analysis():
        """
        Uses TextBlob's rule-based API to conduct sentiment analysis. Adds score to new column in data.
        return: pd.DataFrame
        """
        # setup
        text = data['article_text_clean']
        score = []
        
        for sentence in text:
            sentence = TextBlob(sentence)
            x = sentence.sentiment
            x = sentence.sentiment.polarity
            score.append(x)

        data['score'] = score

        # Convert float score to category based on binning to get 5 levels
        data['sentiment'] = pd.cut(data['score'],
                            bins=5,
                            labels=[1, 2, 3, 4, 5])
        data['sentiment'] = pd.to_numeric(data['sentiment'])
        data = data.drop('score', axis=1)

    def outlet_sentiment():
        """
        Calculates the sentiment score breakdown as a percent per outlet.
        return: list, dictionary
        """
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

        category_names = ['Extremely negative', 'Negative','Neutral', 'Positive', 'Extremely positive']
        publishers = {
            'AP': [AP_1, AP_2, AP_3, AP_4, AP_5],
            'Breitbart': [Breitbart_1, Breitbart_2, Breitbart_3, Breitbart_4, Breitbart_5],
            'Fox': [Fox_1, Fox_2, Fox_3, Fox_4, Fox_5],
            'Buzzfeed': [buzzfeed_1, buzzfeed_2, buzzfeed_3, buzzfeed_4, buzzfeed_5],
            'NBC': [nbc_1, nbc_2, nbc_3, nbc_4, nbc_5],
            'New York Times': [new_york_times_1, new_york_times_2, new_york_times_3, new_york_times_4, new_york_times_5],
            'Politico': [politico_1, politico_2, politico_3, politico_4, politico_5],
            'Washington Times': [washington_times_1, washington_times_2, washington_times_3, washington_times_4, washington_times_5]
        }

        return category_names, publishers

    def outlet_sentiment_plot(publishers, category_names):
        """
        Plots the percent count of sentiment scores per outlet. 
        return: series of subplots
        """
        labels = list(publishers.keys())
        data = np.array(list(publishers.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)
            xcenters = starts + widths / 2

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                ax.text(x, y, str("{0:.0%}".format(c)), ha='center', va='center',
                        color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')

        return fig, ax

        outlet_sentiment_plot(publishers, category_names)
        plt.savefig('sentiment_count.png', bbox_inches='tight')

    def candidate_sentiment():
        """
        Calculates the sentiment averages accross all candidates, per candidate and per candidate and outlet.
        return: a series of lists
        """
        # total average
        sent_mean = data['sentiment'].mean()

        #trump
        trump = data.loc[data['Trump'] == 1]
        trump_sent_mean = trump['sentiment'].mean()
        trump_sentiment = trump.groupby('publisher')['sentiment'].mean().reset_index()

        #sanders
        sanders = data.loc[data['Sanders'] == 1]
        sanders_sent_mean = sanders['sentiment'].mean()
        sanders_sentiment = sanders.groupby('publisher')['sentiment'].mean().reset_index()

        #biden
        biden = data.loc[data['Biden'] == 1]
        biden_sent_mean = biden['sentiment'].mean()
        biden_sentiment = biden.groupby('publisher')['sentiment'].mean().reset_index()

        return sent_mean, trump, trump_sent_mean, trump_sentiment, sanders, sanders_sent_mean, sanders_sentiment, biden, biden_sent_mean, biden_sentiment

    def candidate_sentiment_plot():
        """
        Plots difference in each candidate's sentiment average to overall sentiment mean.
        return: bar plot
        """
        sentiment = [trump_sent_mean - sent_mean,
                     sanders_sent_mean - sent_mean, 
                     biden_sent_mean - sent_mean, 
                     warren_sent_mean - sent_mean, 
                     buttigieg_sent_mean - sent_mean, 
                     bloomberg_sent_mean - sent_mean, 
                     klobuchar_sent_mean - sent_mean, 
                     yang_sent_mean - sent_mean, 
                     steyer_sent_mean - sent_mean, 
                     gabbard_sent_mean - sent_mean]
        candidates = ('trump', 'sanders', 'biden', 'warren', 'buttigieg', 'bloomberg','klobuchar', 'yang', 'steyer', 'gabbard')

        colors = ["darkslategrey", "teal", "steelblue", "slategrey", "lightsteelblue", "blanchedalmond", "lightsalmon", "coral", "tomato", "firebrick"]

        plt.bar(candidates, sentiment, color=colors)
        plt.xticks(candidates)
        plt.xticks(rotation=45)
        plt.show()
        plt.text(x=-0.8, y=-.091, s="Average Sentiment:" + str(sent_mean), horizontalalignment='left')

    def trump_sentiment_plot():
        """
        Plots difference in Trump's sentiment average per publisher to his overall sentiment mean.
        return: bar plot
        """
        sentiment = trump_sentiment['sentiment'] - trump_sent_mean
        outlet = trump_sentiment['publisher']

        plt.bar(outlet, sentiment, color = "firebrick") 
        plt.xticks(outlet)
        plt.xticks(rotation=45)
        plt.suptitle('Trump: Sentiment by Publisher', fontsize=16)
        plt.text(x=-0.8, y=-.091, s="Trump's sentiment mean:" + str(trump_sent_mean), horizontalalignment='left')
        plt.text(x=-0.8, y=-.1, s="Number of Trump sentences:" + str(len(trump)), horizontalalignment='left')

        plt.savefig('trump.png', bbox_inches='tight')

    def sanders_sentiment_plot():
        """
        Plots difference in Sander's sentiment average per publisher to his overall sentiment mean.
        return: bar plot
        """
        sentiment = sanders_sentiment['sentiment'] - sanders_sent_mean
        outlet = sanders_sentiment['publisher']

        plt.bar(outlet, sentiment, color = "tomato") 
        plt.xticks(outlet)
        plt.xticks(rotation=45)
        plt.suptitle('Sanders: Sentiment by Publisher', fontsize=16)
        plt.text(x=-0.8, y=-.16, s="Sanders's sentiment mean:" + str(sanders_sent_mean), horizontalalignment='left')
        plt.text(x=-0.8, y=-.17, s="Number of Sanders sentences:" + str(len(sanders)), horizontalalignment='left')

        plt.savefig('sanders.png', bbox_inches='tight')

    def biden_sentiment_plot():
        """
        Plots difference in Biden's sentiment average per publisher to his overall sentiment mean.
        return: bar plot
        """
        sentiment = biden_sentiment['sentiment'] - biden_sent_mean
        outlet = biden_sentiment['publisher']

        plt.bar(outlet, sentiment, color = "coral") 
        plt.xticks(outlet)
        plt.xticks(rotation=45)
        plt.suptitle('Biden: Sentiment by Publisher', fontsize=16)
        plt.text(x=-0.8, y=-.13, s="Biden's sentiment mean:" + str(biden_sent_mean), horizontalalignment='left')
        plt.text(x=-0.8, y=-.14, s="Number of Biden sentences:" + str(len(biden)), horizontalalignment='left')

        plt.savefig('biden.png', bbox_inches='tight')

    def sentiment_time():
        """
        Calculates the mean sentiment score per candidate per day.
        return: DataFrame
        """
        warnings.simplefilter(action='ignore')
        # filter sentences only about one candidate
        candidate_sentiment = data.loc[data['candidates_mentioned'] == 1]

        # create new column with candidate name
        candidate_sentiment['candidate'] = candidate_sentiment['article_text'].str.extract('({})'.format('|'.join(candidates)),
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

        return mean_per_day

    def sentiment_time_plot():
        """
        Plots sentiment scores per candidate over time
        return: bar plot
        """
        chart = sns.lineplot(x = 'date', y = 'sentiment', hue = 'candidate', data = mean_per_day)
        plt.setp(chart.get_xticklabels(), rotation = 45)
        plt.setp(chart.get_xticklabels(), rotation = 45)
        plt.title('Average Sentiment Over Time')
        plt.title('Average Sentiment Over Time')
        chart.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), ncol=1)
        plt.savefig('sentiment_time.png', bbox_inches='tight')

