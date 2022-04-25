import json
import zipfile
import pandas as pd
from sympy import source
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

    def find_created_time(self) -> list:
        created_at = []
        for tweet in self.tweets_list:
            created_at.append(tweet[created_at])

        return created_at

    def find_source(self) -> list:
        source = []
        for tweet in self.tweets_list:
            source.append(tweet[source])

        return source

    def find_screen_name(self) -> list:
        screen_name = []
        for tweet in self.tweets_list:
            screen_name.append(tweet['user']['screen_name'])

        return screen_name

    def find_followers_count(self) -> list:
        followers_count = []
        for tweet in self.tweets_list:
            followers_count.append(tweet['user']['follower_count'])

        return followers_count

    def find_friends_count(self) -> list:
        friends_count = []
        for tweet in self.tweets_list:
            friends_count.append(tweet['user']['friends_count'])

        return friends_count

    def is_sensitive(self) -> list:
        is_sensitive = []
        for tweet in self.tweets_list:
            if 'possibly_sensitive' in tweet.keys():
                is_sensitive.append(tweet['possibly_sensitive'])
            else:
                is_sensitive.append(None)

        return is_sensitive

    def find_favourite_count(self) -> list:
        favorite_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                favorite_count.append(
                    tweet['retweeted_status']['favorite_count'])
            else:
                favorite_count.append(0)

        return favorite_count

    def find_retweet_count(self) -> list:

        retweet_count = []
        for tweet in self.tweets_list:
            if 'retweeted_status' in tweet.keys():
                retweet_count.append(
                    tweet['retweeted_status']['retweet_count'])
            else:
                retweet_count.append(0)

        return retweet_count

    def find_hashtags(self) -> list:
        hashtags = []
        for tweet in self.tweets_list:
            if len(tweet['entities']['hashtags']) > 0:
                hashtags.append(','.join([x['text']
                                for x in tweet['entities']['hashtags']]))
            else:
                hashtags.append('')
        return hashtags


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data\Economic_Twitter_Data.zip")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
