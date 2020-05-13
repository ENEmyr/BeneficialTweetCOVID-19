import json
from codecs import open
from utils.jsonTweetEncoder import JSONEncoder
from twitterscraper import query_tweets
from os.path import join, abspath

def scrape(query_string = '(#COVID19,#COVID-19,#COVID_19)', limit=1, lang='th', poolsize=1, file_name = 'covid19_raw_dataset', save = True):
    tweets_lst = query_tweets(query_string, limit=limit, lang=lang, poolsize=poolsize)
    print("No.tweets = {}".format(len(tweets_lst)))
    if save:
        with open(abspath(join('dataset', file_name+'.json')), 'w', encoding='utf-8-sig') as f:
            json.dump(tweets_lst, f, cls=JSONEncoder, ensure_ascii=False, indent=3)
    else:
        return tweets_lst