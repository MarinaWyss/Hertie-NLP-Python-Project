# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import seaborn as sns


class Descriptives:
    """
    Creates descriptive plots.
    """
    def __init__(self):
        self.candidates = ['Trump', 'Sanders', 'Biden', 'Warren', 'Buttigieg', 
                           'Bloomberg', 'Klobuchar', 'Yang', 'Steyer', 'Gabbard']
        self.path = '/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/'
        self._sentence_data = None
        self._total_candidate_mentions = None
        self._mentions_over_time = None
    
    def sentence_data(self):
        """
        Reads in and prepares the sentence data
        return: pd.DataFrame
        """
        sentence_data = pd.read_csv(self.path + 'data/sentence_data.csv')
        
        # convert date to datetime
        sentence_data['date'] = pd.to_datetime(sentence_data['date'], errors='coerce')
        sentence_data['date'] = sentence_data['date'].dt.date
        
        # filtering weird dates
        mask = (sentence_data['date'].astype('str') >= "2020-03-01") & (sentence_data['date'].astype('str') < "2020-04-03")
        sentence_data = sentence_data.loc[mask]
        
        self._sentence_data = sentence_data
        
        return self._sentence_data
    
    def total_candidate_mentions(self):
        """
        Calculates total mentions per candidate
        return: pd.DataFrame
        """
        total_candidate_mentions = self.sentence_data().loc[:, self.candidates].sum(axis = 0, skipna = True)
        total_candidate_mentions = total_candidate_mentions.to_frame(name = 'count').rename_axis('candidate').reset_index()
        
        self._total_candidate_mentions = total_candidate_mentions
        
        return self._total_candidate_mentions
    
    def mentions_over_time(self):
        """
        Calculates total mentions per candidate per day
        return: pd.DataFrame
        """
        self.candidates.append('date')
        time_data = self.sentence_data().loc[:, self.candidates]
        
        # total mentions per candidate per day
        sum_cand_day = time_data.groupby(['date']).sum()
        sum_cand_day.reset_index(inplace = True)
        
        # wide to long
        sum_cand_day_long = pd.melt(sum_cand_day,
                                    id_vars=['date'],
                                    var_name='candidates', 
                                    value_name='count')
        
        self._mentions_over_time = sum_cand_day_long
        
        return self._mentions_over_time
    
    def candidate_mentions_plot(self, fig_out):
        """
        Creates a barplot of the total candidate mentions 
        return: barplot
        """
        chart = sns.barplot(x = 'count', y = 'candidate', 
                            data = self.total_candidate_mentions())
        plt.setp(chart.get_yticklabels(), rotation = 40)
        plt.title('Total Candidate Mentions - Sentence-level')

        if fig_out is True:
            plt.savefig(self.path + 'figures/candidate_mentions.png', dpi = 400)
        
    def dem_mentions_plot(self, fig_out):
        """
        Creates a barplot of the total candidate mentions, excluding Trump
        return: barplot
        """
        # filter out Trump
        total_candidate_mentions = self.total_candidate_mentions()
        mentions_no_trump = total_candidate_mentions[total_candidate_mentions['candidate'] != 'Trump']
        
        # plot
        chart = sns.barplot(x = 'count', y = 'candidate', data = mentions_no_trump)
        plt.setp(chart.get_yticklabels(), rotation = 40)
        plt.title('Total Candidate Mentions (Democrats Only) - Sentence-level')

        if fig_out is True:
            plt.savefig(self.path + 'figures/dem_mentions.png', dpi = 400)
        
    def candidate_time_plot(self, fig_out):
        """
        Creates a line of the total candidate mentions over time
        return: lineplot
        """
        chart = sns.lineplot(x = 'date', y = 'count', 
                             hue = 'candidates', 
                             data = self.mentions_over_time())
        plt.setp(chart.get_xticklabels(), rotation = 60)
        plt.title('Total Candidate Mentions Over Time - Sentence-level')
        chart.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), ncol=1)
        date_form = DateFormatter("%m-%d")
        chart.xaxis.set_major_formatter(date_form)

        if fig_out is True:
            plt.savefig(self.path + 'figures/candidate_time_plot.png', dpi = 400, bbox_inches = 'tight')
        
    def dem_time_plot(self, fig_out):
        """
        Creates a line of the total candidate mentions over time, excluding Trump
        return: lineplot
        """
        # filter out Trump
        mentions_over_time = self.mentions_over_time()
        mentions_time_dems = mentions_over_time[mentions_over_time['candidates'] != 'Trump']

        # plot
        chart = sns.lineplot(x = 'date', y = 'count', 
                             hue = 'candidates', 
                             data = mentions_time_dems)
        plt.setp(chart.get_xticklabels(), rotation = 60)
        plt.title('Total Candidate Mentions Over Time (Democrats Only) \nSentence-level')
        chart.legend(loc='center right', bbox_to_anchor=(1.3, 0.5), ncol=1)
        date_form = DateFormatter("%m-%d")
        chart.xaxis.set_major_formatter(date_form)

        if fig_out is True:
            plt.savefig(self.path + 'figures/dem_time_plot.png', dpi = 400, bbox_inches = 'tight')

