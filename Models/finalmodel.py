from joblib import dump
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from time import time
from sklearn.pipeline import Pipeline
from pprint import pprint
from sklearn.model_selection import GridSearchCV
import sys

kNB = "https://raw.githubusercontent.com/krisshbhargava/flask_Priorit.ai/refs/heads/main/Models/Training%20Data/kitchenAndBath.csv"
rI = "https://raw.githubusercontent.com/krisshbhargava/flask_Priorit.ai/refs/heads/main/Models/Training%20Data/roomIssue.csv"
elc = "https://raw.githubusercontent.com/krisshbhargava/flask_Priorit.ai/refs/heads/main/Models/Training%20Data/electrical.csv"

kitchenDF = pd.read_csv(kNB)
roomDF = pd.read_csv(rI)
electricalDF = pd.read_csv(elc)

def save_model_and_vect(df, modelName, vecName):
    X_train, X_test, y_train, y_test = train_test_split(
        df['Complaint'], df['Issue'], shuffle=True, test_size=0.2, random_state=None)

    tfidf = TfidfVectorizer(sublinear_tf=True,
                            min_df=4,
                            max_df=0.6,
                            norm='l1',
                            ngram_range=(1, 2),
                            stop_words='english')

    X_train_counts = tfidf.fit_transform(X_train)
    X_test_counts = tfidf.transform(X_test)

    model = MultinomialNB(alpha=1e-04)
    model.fit(X_train_counts, y_train)

    dump(model, modelName)
    dump(tfidf, vecName)
    
save_model_and_vect(kitchenDF, "kitchen_model.joblib", "kitchen_vec.joblib")
save_model_and_vect(roomDF, "room_model.joblib", "room_vec.joblib")
save_model_and_vect(electricalDF, "electrical_model.joblib", "electrical_vec.joblib")
