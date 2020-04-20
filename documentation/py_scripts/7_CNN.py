#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import re
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

import transformers

from sklearn.metrics import classification_report

class KimCNN(nn.Module):
    """
    CNN for binary classification of BERT-embedding sentences
    """
    def __init__(self, embed_num, embed_dim, class_num, kernel_num, kernel_sizes, dropout, static):
        super(KimCNN, self).__init__()
        V = embed_num
        D = embed_dim
        C = class_num
        Co = kernel_num
        Ks = kernel_sizes
        
        self.static = static
        self.embed = nn.Embedding(V, D)
        self.convs1 = nn.ModuleList([nn.Conv2d(1, Co, (K, D)) for K in Ks])
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(len(Ks) * Co, C)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        if self.static:
            x = Variable(x)
        x = x.unsqueeze(1)  
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs1]  
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]  
        x = torch.cat(x, 1) 
        x = self.dropout(x)  
        logit = self.fc1(x)  
        output = self.sigmoid(logit) 
        return output
