import requests, re
from codecs import open
from os.path import join, abspath
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote

def get_url_title(urls):
    titles = []
    for url in urls:
        try:
            res = requests.get(url)
            soup = bs(res.content, 'lxml')
            titles.append(soup.select_one('title').text)
        except: # sometimes the title is None will cause error
            pass
    return titles

def scrape(url):
    url_matcher = re.compile(r'(http://|https://|https://www\.|http://www\.)twitter\.com/.+/status/[0-9]{19}(/|)$').match
    noise_cut_pattern = r'[^a-zA-Z0-9ก-๙| ]+'
    links_pattern = r'https://t\.co/[a-zA-Z0-9]{10}(/|)'
    hashtags_pattern = r'#.+( )'
    if bool(url_matcher(url)):
        res = requests.get(url)
        soup = bs(res.content, 'lxml')
        tweet_text = soup.select_one('title').text
        link = re.search(links_pattern, tweet_text)
        if link != None:
            link = link.group()
        tweet_text = re.sub(links_pattern, '', tweet_text.rstrip())
        tweet_text = re.sub(hashtags_pattern, '', tweet_text.rstrip())
        tweet_text = ''.join(tweet_text.split(':')[1:]) # trim username
        tweet_text += ' '.join(get_url_title([link]))
        tweet_text = re.sub(noise_cut_pattern, '', tweet_text)
        return tweet_text
    else:
        raise ValueError('Invalid tweet url')
