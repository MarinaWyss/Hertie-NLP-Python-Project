# coding: utf-8

import pandas as pd
import numpy as np
import re
import torch
import transformers 

import nltk
from nltk.corpus import stopwords


class BERT:
    """
    Reads in sentence-level data. 
    Filters for sentences related to Biden or Sanders. 
    Removes the candidate names from the text and moves them to a new label column.
    Applies BERT embeddings 
    return: BERT embedded train, test, and val datasets, as train, test, and val labels
    """
    
    def __init__(self):
        self.candidates = ['Trump', 'Bernie', 'Sanders', 'Biden', 'Warren', 'Buttigieg', 'Bloomberg', 
                           'Klobuchar', 'Yang', 'Steyer', 'Gabbard']
        self._data = pd.read_csv('/Users/marinabennett/Desktop/Hertie/1._Spring_2020/Hertie-NLP-Python-Project/data/sentence_data.csv')
        self._prepped_data = None

    def data(self):
        """
        Removes candidate names from the text and uses names to create a label column.
        Filters for Sanders and Biden.
        return: pd.DataFrame
        """
        data = self._data.sample(frac = 1)
        data = data.sample(n = 1000)
        data = data.loc[data['candidates_mentioned'] == 1][['article_text']]
        
        # add labels
        data['label'] = data['article_text'].str.extract('({})'.format('|'.join(self.candidates)), 
                            flags = re.IGNORECASE, expand = False).str.lower().fillna('')
        data['label'] = np.where(data['label'].str.contains('bernie'), 'sanders', data['label'])

        # filter data set
        data = data.loc[data['label'].isin(['biden', 'sanders'])]

        # remove candidate names
        data['article_text'] = data['article_text'].str.replace('Bernie', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Bernard', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Sanders', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Senator', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Joe', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Biden', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Vice President', '[candidate]')
        
        data = data.drop_duplicates()
        
        # label to numeric
        data['label'] = np.where(data['label'] == "sanders", 1, 0)

        self._data = data

        return self._data
    
    def prepped_data(self):
        """
        Prepares the article text for the BERT embeddings
        return: pd.DataFrame
        """
        data = self.data()
        
        sentences = data['article_text']

        # lowercase everything
        sentences = [sentences.lower() for sentences in sentences]

        # remove punctuation
        sentences = [re.sub(r'[^\w\s]','',s) for s in sentences]

        # remove numbers
        sentences = [re.sub('[0-9]','', s) for s in sentences]

        # remove stopwords
        clean = []
        for item in sentences:
            for word in stopwords.words('english'):
                item = item.replace(" " + word + " ", ' ')
            clean.append(item)

        data['article_text'] = clean
        
        self._prepped_data = data
        
        return self._prepped_data
    
    def train_test_split(self):
        """
        Selects a random sample of the prepped data for the train, val, and test datasets
        return: pd.DataFrame
        """
        # shuffle
        np.random.seed(42)
        data = self.prepped_data().sample(frac = 1)
        data = data.reset_index(drop = True)

        # small sample for training and reshuffle again
        sample_data = data.groupby('label').apply(pd.DataFrame.sample, n = 100, replace = True)
        sample_data = sample_data.sample(frac = 1)
        sample_data = sample_data.reset_index(drop = True)
        
        # train test split
        df_train = sample_data[:70].reset_index(drop=True)
        df_val = sample_data[70:90].reset_index(drop=True)
        df_test = sample_data[90:100].reset_index(drop=True)
        
        return df_train, df_val, df_test
        

    def bert_model(self):
        """
        Creates the BERT model to apply BERT embeddings.
        return: BERT embedding datasets
        """
        # import model and tokenizer
        model_class = transformers.BertModel
        tokenizer_class = transformers.BertTokenizer
        pretrained_weights = 'bert-base-uncased'

        # Load pretrained model/tokenizer
        tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
        bert_model = model_class.from_pretrained(pretrained_weights)

        # grab data
        df_train, df_val, df_test = self.train_test_split()
        
        # max seq. is longest sentence in characters
        max_seq = max( 
            df_train['article_text'].str.len().max(),
            df_val['article_text'].str.len().max(),
            df_test['article_text'].str.len().max()
        )
        
        # transform each sentence into a 2D matrix
        def tokenize_text(df, max_seq):
            return [tokenizer.encode(text, add_special_tokens=True)[:max_seq] for text in df.article_text.values]

        def pad_text(tokenized_text, max_seq):
            return np.array([el + [0] * (max_seq - len(el)) for el in tokenized_text])

        def tokenize_and_pad_text(df, max_seq):
            tokenized_text = tokenize_text(df, max_seq)
            padded_text = pad_text(tokenized_text, max_seq)
            return torch.tensor(padded_text)

        def targets_to_tensor(df, target_columns):
            return torch.tensor(df[target_columns].values, dtype=torch.float32)
        
        # tokenize and pad text
        train_indices = tokenize_and_pad_text(df_train, max_seq)
        val_indices = tokenize_and_pad_text(df_val, max_seq)
        test_indices = tokenize_and_pad_text(df_test, max_seq)
        
        # create BERT embeddings for features
        with torch.no_grad():
            x_train = bert_model(train_indices)[0] 
            x_val = bert_model(val_indices)[0] 
            x_test = bert_model(test_indices)[0]

        target_columns = "label"

        # transform labels into tensors
        y_train = targets_to_tensor(df_train, target_columns)
        y_val = targets_to_tensor(df_val, target_columns)
        y_test = targets_to_tensor(df_test, target_columns)
        
        return x_train, x_val, x_test, y_train, y_val, y_test

