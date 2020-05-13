import re
import time
from optparse import OptionParser
from beneficialtweets import train, predict
from utils import ProgressBarThread

parser = OptionParser()

parser.add_option('--train', dest='train', help='Build the classifier from given dataset', default='')
parser.add_option('--predict', dest='predict', help='Classify tweet from given text or tweet_url', default='')
parser.add_option('--query_tweets', dest='query_tweets', help='Fetch all tweets acording to given scrape parameter.\nSend scrape parameter by writting a string that can be converted into dictionary.\nA list of acceptable dictionary keys : ["query_string", "limit", "lang", "poolsize", "file_name", "save"]\n', default='')
parser.add_option('-p', '--pos_tweets', dest='pos_path', help='Path to positive tweets dataset, required when train = true', default='')
parser.add_option('-n', '--neg_tweets', dest='neg_path', help='Path to negative tweets dataset, required when train = true', default='')
parser.add_option('-r', '--ratio', dest='ratio', help='Train test split ratio, optional when train = true', default='')
parser.add_option('-a', '--algorithms', dest='algorithms', help='Classifier algorithm ("all", "tf", "svm"), required when train = true', default='')
parser.add_option('-m', '--model', dest='model', help='Classifier model load path, optional if not specific default model(random forest) will be use', default='')

if __name__ == '__main__':
    progress_bar = ProgressBarThread('Computing')
    (options, args) = parser.parse_args()
    if options.train or options.predict:
        if options.train:
            if options.pos_path and options.neg_path:
                args = [options.pos_path, options.neg_path]
                if options.ratio:
                    args.append(float(options.ratio))
                else:
                    args.append(.3)
                if options.algorithms and options.algorithms in ['all', 'svm', 'tf']:
                    args.append(options.algorithms)
                else:
                    args.append('all')
                progress_bar.start()
                train(*args)
                progress_bar.stop()
            else:
                raise SyntaxError("Required both of positive and negative datasets")
        elif options.predict:
            tweet_url_matcher = re.compile(r'^(http://|https://|https://www\.|http://www\.)twitter\.com/.+/status/[0-9]{19}(/|)$').match
            if bool(tweet_url_matcher(options.predict)):
                from scraper import tweet
                tweet_text = tweet.scrape(options.predict)
            else:
                tweet_text = options.predict
            progress_bar.start()
            if options.model:
                pred_class = predict(tweet_text, options.model)
            else:
                pred_class = predict(tweet_text)
            time.sleep(.1)
            print(f'\nText : {tweet_text}\nClass : {pred_class}')
            progress_bar.stop()
    elif options.query_tweets:
        from scraper import tweets
        args = []
        args_dict = eval(options.query_tweets)
        if not isinstance(args_dict, dict):
            raise ValueError('query_tweets parameter must be a string in dictionary form')
        if 'query_string' in args_dict.keys():
            args.append(args_dict['query_string'])
        else:
            args.append('(#COVID19,#COVID-19,#COVID_19)')
        if 'limit' in args_dict.keys():
            args.append(args_dict['limit'])
        else:
            args.append(1)
        if 'lang' in args_dict.keys():
            args.append(args_dict['lang'])
        else:
            args.append('th')
        if 'poolsize' in args_dict.keys():
            args.append(args_dict['poolsize'])
        else:
            args.append(1)
        if 'file_name' in args_dict.keys():
            args.append(args_dict['file_name'])
        else:
            args.append('covid19_raw_dataset')
        if 'save' in args_dict.keys():
            args.append(args_dict['save'])
        else:
            args.append(True)
        progress_bar.start()
        tweets.scrape(*args)
        progress_bar.stop()
    else:
        raise SyntaxError("Required train, predict or query_tweets argument")
