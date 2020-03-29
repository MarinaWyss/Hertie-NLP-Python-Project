import pandas as pd
import numpy as np
import re
import torch
from transformers import BertTokenizer, BertModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

filepath = 'C:/Users/lmwyss/Desktop/Hertie-NLP-Python-Project/data'


class Bert:

    def __init__(self):
        self.candidates = ['Trump', 'Bernie', 'Sanders', 'Biden', 'Warren',
                           'Buttigieg', 'Bloomberg', 'Klobuchar', 'Yang',
                           'Steyer', 'Gabbard']
        self._data = None
        self._bert_model = None

    def data(self):
        data = pd.read_csv(filepath + '/sentence_data.csv')[['article_text']]

        # add labels
        data['label'] = data['article_text'].str.extract('({})'.format('|'.join(self.candidates)),
                                                         flags=re.IGNORECASE, expand=False).str.lower().fillna('')
        data['label'] = np.where(data['label'].str.contains('bernie'), 'sanders', data['label'])

        # filter candidates
        data = data.loc[data['label'].isin(['biden', 'sanders'])]

        # remove candidate names
        data['article_text'] = data['article_text'].str.replace('Donald', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Trump', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Bernie', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Sanders', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Joe', '[candidate]')
        data['article_text'] = data['article_text'].str.replace('Biden', '[candidate]')

        self._data = data

        return self._data

    def bert_model(self):
        # sampling data for baseline
        sample_data = self.data().groupby('label').apply(pd.DataFrame.sample, n=500)

        # tokenization
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        tokenized = sample_data["article_text"].apply(
            (lambda x: tokenizer.encode(x, add_special_tokens=True, max_length=511))
        )

        # padding
        max_len = 0
        for i in tokenized.values:
            if len(i) > max_len:
                max_len = len(i)

        padded_text = np.array([i + [0] * (max_len - len(i)) for i in tokenized.values])

        # attention mask
        attention_mask = np.where(padded_text != 0, 1, 0)
        attention_mask = torch.tensor(attention_mask)

        # input ids
        input_ids = torch.tensor(padded_text).to(torch.int64)

        # modeling
        model = BertModel.from_pretrained('bert-base-uncased')

        with torch.no_grad():
            last_hidden_states = model(input_ids, attention_mask=attention_mask)

        # extract features and labels
        features = last_hidden_states[0][:, 0, :].numpy()
        labels = sample_data['label']

        # train test split
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels)

        # basic logistic regression model
        lr_clf = LogisticRegression()
        lr_clf.fit(train_features, train_labels)

        # accuracy
        lr_clf.score(test_features, test_labels)
        preds = lr_clf.predict(test_features)

        self._bert_model = classification_report(preds, test_labels)

        return self._bert_model
