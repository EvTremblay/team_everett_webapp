"""Evaluate feature importance"""
from __future__ import division, print_function, absolute_import

# Pandas/Numpy
import pandas as pd
import numpy as np

# Models
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression

# Load data
X = pd.read_pickle('../data/X.pkl')
y = pd.read_csv('../data/y_vector.csv', header=None, names=('Fraud'))

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=55)

# One-in
scores = []
for i, c in enumerate(X.columns):
    # Fit model
    m = LogisticRegression().fit(X_train[c].reshape(-1, 1), y_train)
    scores[i] = m.score(X_test[c].reshape(-1, 1), y_test)

model_scores = zip(columns, scores)

ms = pd.DataFrame(model_scores, columns=['model', 'score'])
ms.to_pickle('../data/col_scores.pkl')
ms.to_csv('../data/col_scores.csv')
