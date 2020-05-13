<h1 align="center">BeneficialTweetCOVID-19</h1>

<p align="center">
<img src="https://i.imgur.com/pwLu87p.jpg" alt="NewsSummarizeSystem"></p>

> #### Build a classifier that can extract a useful Thai tweet among a ton of tweets during COVID-19 epidemic.

> ##### **Please note that the model was trained by using a sentence vector that converted by Thai word embedding model, hence this model can't be use in other language except Thai*

![](https://img.shields.io/github/stars/Untesler/BeneficialTweetCOVID-19.svg?style=social&label=Star&maxAge=2592000) 
![](https://img.shields.io/github/forks/Untesler/BeneficialTweetCOVID-19.svg?style=social&label=Fork&maxAge=2592000) 
![](https://img.shields.io/github/watchers/Untesler/BeneficialTweetCOVID-19.svg?style=social&label=Watch&maxAge=2592000) ![](https://img.shields.io/github/tag/Untesler/BeneficialTweetCOVID-19.svg) 
![](https://img.shields.io/github/release/Untesler/BeneficialTweetCOVID-19.svg) 

## Setup dependencies
- To install dependencies -> `pip install -r requirements.txt`

## Training the model
- Firstly, Building a raw dataset by scrape tweets data.

``` bash
python main.py --query_tweets="
    {
        'query_string': '<twitter_query_string>', 
        'lang': '<specific_a_language_of_tweets>', 
        'poolsize': <a_pool_size_for_pararel_scraping>, 
        'limit': <query_limit>, 
        'file_name': '<save_file_name>',
    }"
```
- Next, Create a label file that used to map the manually label to the raw dataset, for the details please look at the ```./notebooks/1_Create_Unlabel_Dataset.ipynb```  file.
- Then, Map the class from manually labeled file in the previous step to the raw dataset and clean the data then save the cleaned dataset separately into positive tweets file('useful-tweets.json' by default) and negative tweets file('useless-tweets.json' by default), for the details please look at the ```./notebooks/2_Data_Preparation.ipynb``` file.
- Train the model by
``` bash
python main.py --train=true -p "dataset/useful-tweets.json" -n "dataset/useless-tweets.json" -r .3 -a "all"
```
- The model will save into ``` ./dataset/ ``` directory by default

## Testing the model
- Predict a class of the tweet by
``` bash
python main.py --predict="<tweet_url>"
```
or
``` bash
python main.py --predict="<tweet_text>"
```

## Accuracy Score
- Support vector machine algorithm : 93.287%
- Random forest algorithm : 94.444%

## Help main.py
``` bash
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  --train=TRAIN         Build the classifier from given dataset
  --predict=PREDICT     Classify tweet from given text or tweet_url
  --query_tweets=QUERY_TWEETS
                        Fetch all tweets acording to given scrape parameter.
                        Send scrape parameter by writting a string that can be
                        converted into dictionary. A list of acceptable
                        dictionary keys : ["query_string", "limit", "lang",
                        "poolsize", "file_name", "save"]
  -p POS_PATH, --pos_tweets=POS_PATH
                        Path to positive tweets dataset, required when train =
                        true
  -n NEG_PATH, --neg_tweets=NEG_PATH
                        Path to negative tweets dataset, required when train =
                        true
  -r RATIO, --ratio=RATIO
                        Train test split ratio, optional when train = true
  -a ALGORITHMS, --algorithms=ALGORITHMS
                        Classifier algorithm ("all", "tf", "svm"), required
                        when train = true
  -m MODEL, --model=MODEL
                        Classifier model load path, optional if not specific
                        default model(random forest) will be use
```

*Written in Python version 3.8.2*

## Authors
* ENEmy ([@ENE_mee](https://twitter.com/ENE_mee))

