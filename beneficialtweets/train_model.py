import random, json, time
import numpy as np
from codecs import open
from joblib import dump
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from os.path import abspath, join
from utils import clean_text, sentence_vectorizer 

def load_dataset(pos_dataset_path, neg_dataset_path):
    dataset = []
    with open(abspath(join(*pos_dataset_path)), 'r', encoding='utf-8-sig') as f:
        positive_tweets_json = json.load(f)
    with open(abspath(join(*neg_dataset_path)), 'r', encoding='utf-8-sig') as f:
        negative_tweets_json = json.load(f)
    for index in range(max(len(positive_tweets_json), len(negative_tweets_json))):
        if index < len(positive_tweets_json):
            # clean text
            text = clean_text(positive_tweets_json[index]['text'])
            # convert a Thai sentence into vector shape (1, 300)
            vect = sentence_vectorizer(text)
            dataset.append((vect, 1))
        if index < len(negative_tweets_json):
            # clean text
            text = clean_text(negative_tweets_json[index]['text'])
            # convert a Thai sentence into vector shape (1, 300)
            vect = sentence_vectorizer(text)
            dataset.append((vect, 0))
    random.shuffle(dataset)
    return np.array([X[0] for X in dataset]), np.array([y[1] for y in dataset])

def train(
    pos_dataset_path,
    neg_dataset_path,
    train_test_ratio = .3,
    algorithms = 'all'):
    if algorithms.lower() not in ['all', 'svm', 'tf']:
        raise ValueError('Unsupported algorithm')
    svm_acc, tf_acc = None, None
    pos_dataset_path = pos_dataset_path.split('/')
    neg_dataset_path = neg_dataset_path.split('/')

    X, y = load_dataset(pos_dataset_path, neg_dataset_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
    X_train, X_test = X_train.reshape(-1, X_train.shape[2]), X_test.reshape(-1, X_test.shape[2])
    if algorithms.lower() == 'svm' or algorithms.lower() == 'all':
        # Support vector machine classifier
        clf = svm.SVC(C = 5.0, kernel = 'rbf')
        clf.fit(X_train, y_train)
        # Predict the labels on validation dataset
        y_pred = clf.predict(X_test)
        svm_acc = accuracy_score(y_test, y_pred) * 100
        dump(clf, abspath(join('model', 'svm_classifier.joblib'))) # save model
    if algorithms.lower() == 'tf' or algorithms.lower() == 'all':
        # Random Forest classifier
        clf = RandomForestClassifier(max_depth=11, criterion='entropy')
        clf.fit(X_train, y_train)
        # Predict the labels on validation dataset
        y_pred = clf.predict(X_test)
        tf_acc = accuracy_score(y_test, y_pred) * 100
        dump(clf, abspath(join('model', 'rf_classifier.joblib'))) # save model
    print(f'\nX_train shape : {X_train.shape}\nX_test shape : {X_test.shape}\n')
    if svm_acc != None:
        print(f'Support Vector Machine Accuracy Score = {svm_acc}')
    if tf_acc != None:
        print(f'Random Forest Accuracy Score = {tf_acc}')