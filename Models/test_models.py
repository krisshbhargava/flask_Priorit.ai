from joblib import load
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

# Load the model
kitchen_model = load('Models/ModelsTrained/kitchen_model.joblib')
kitchen_vec = load('Models/ModelsTrained/kitchen_vec.joblib')
room_model = load('Models/ModelsTrained/room_model.joblib')
room_vec = load('Models/ModelsTrained/room_vec.joblib')
electrical_model = load('Models/ModelsTrained/electrical_model.joblib')
electrical_vec = load('Models/ModelsTrained/electrical_vec.joblib')

# Now you can use the model to make predictions
myTFDIF = TfidfVectorizer(sublinear_tf=True,
                            min_df=4,
                            max_df=0.6,
                            norm='l1',
                            ngram_range=(1, 2),
                            stop_words='english')

def test_reply (order, model, myTFDIF):
    input = np.array([order])
    input_counts = myTFDIF.transform(input)
    y_pred_prob = model.predict_proba(input_counts)
    dict = {}
    categories = model.classes_
    for k in range(len(categories)):
      dict[categories[k]] = y_pred_prob[:, k]
    largest_element = y_pred_prob.max()
    if largest_element >= (3.5/5):
        reply = [model.predict(input_counts)[0], 1]
    elif largest_element >= (2.5/5):
        reply = [model.predict(input_counts)[0], 0]
    else:
        reply = [model.predict(input_counts)[0], -1]
    return reply

def model_reply(student_id, building, category, description):
    if category == "kitchenDF":
        model = kitchen_model
        myTFDIF = kitchen_vec
    elif category == "electricalDF":
        model = electrical_model
        myTFDIF = electrical_vec
    elif category == "roomDF":
        model = room_model
        myTFDIF = room_vec
    my_tup = (student_id, building, category)
    my_tup = my_tup + (test_reply(description, model, myTFDIF)[0], str(test_reply(description, model, myTFDIF)[1]))
    my_tup = my_tup + (description, )
    return my_tup