from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize
from pythainlp.word_vector import sentence_vectorizer
from utils.ProgressBarThread import ProgressBarThread

def remove_duplicated_sent(sentence):
    sents = sentence.split(' ')
    sents = list(dict.fromkeys(sents)) # remove duplicated by keep the order of keys
    return ''.join(sents)

def remove_stopwords(sentence):
    words = list(filter(lambda word: not word in thai_stopwords(), word_tokenize(sentence)))
    return ''.join(words)

def clean_text(sentence, keep_stopwords = True):
    sentence = remove_duplicated_sent(sentence)
    if not keep_stopwords:
        sentence = remove_stopwords(sentence)
    return sentence