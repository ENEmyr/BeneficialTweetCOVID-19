from joblib import load
from os.path import abspath, join
from utils import remove_stopwords, sentence_vectorizer

def predict(sentence, model_path='./model/rf_classifier.joblib'):
    classifier = load(abspath(join(*model_path.split('/'))))
    sentence = remove_stopwords(sentence)
    pred_class = 'BeneficialTweet' if classifier.predict(sentence_vectorizer(sentence))[0] == 1 else 'Non-BeneficialTweet'
    return pred_class