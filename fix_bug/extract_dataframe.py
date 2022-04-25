import json
import zipfile
import pandas as pd
from textblob import TextBlob


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file

    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    with zipfile.ZipFile("json_file", "r") as z:
        for tweets in z.open(json_file, 'r'):
            tweets_data.append(json.loads(tweets.decode("utf-8")))

    return len(tweets_data), tweets_data


class TweetDfExtractor:

    def __init__(self, tweets_list):

        self.tweets_list = tweets_list

    # an example function for
    def find_statuses_count(self) -> list:
        statuses_count = []
        for tweet in self.tweets_list:
            statuses_count.append(tweet['user']['statuses_count'])

        return statuses_count

    def find_full_text(self) -> list:
        """
        The code checks if retweeted stutus is in tweet list 
        Extended tweets in retweeted status
        """
        text = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in self.tweets_list and 'extended_tweet' in tweet['retweeted_status']:
                text.append(tweet['retweeted_status']
                            ['extended_tweet']['full_text'])
            else:
                text.append(['Empty'])
        return text

    def find_sentiments(self, text: list) -> list:
        polarity = []
        subjectivity = []
        for tweet in text:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment
            polarity.append(sentiment.polarity)
            subjectivity.append(sentiment.subjectivity)

        return polarity, subjectivity


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data\Economic_Twitter_Data.zip")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
