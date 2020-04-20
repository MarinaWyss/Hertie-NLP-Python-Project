#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import pandas as pd

import torch
import torch.nn as nn

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report


# (This script uses a tiny test dataset but is scaled up on the full set for our actual project) 


class Feedforward(torch.nn.Module):
    """
    Basic feedforward MLP for binary classification of BERT-embedding sentences
    """
    def __init__(self, input_size, hidden_size):
        super(Feedforward, self).__init__()
        self.input_size = input_size
        self.hidden_size  = hidden_size
        self.fc1 = nn.Linear(self.input_size, self.hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(self.hidden_size, 1)
        self.sigmoid = nn.Sigmoid()
      
    def forward(self, x):
        hidden = self.fc1(x)
        relu = self.relu(hidden)
        output = self.fc2(relu)
        output = self.sigmoid(output)
        return output
