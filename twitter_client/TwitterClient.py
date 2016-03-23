import urllib, urllib2, json, tweepy
from pyquery import PyQuery
from tweepy import OAuthHandler
from tweepy.error import TweepError

class TwitterClient:
    """
    Main class of the Research Software Sentiment Analyser module for querying
    Twitter for reviews on software for research.
    """

    def __init__(self):
        """
        Access Twitter API.
        """
        self.api = self._get_twitter_api()

    def _get_twitter_api(self):
        """
        Loads the secrets.json file and connects to Twitter.
        Since we are only reading public information from Twitter, we don't need
        access token/secret values.
        """
        with open('secrets.json') as secrets_file:
            secrets = json.load(secrets_file)

        consumer_key = secrets['consumer_key']
        consumer_secret = secrets['consumer_secret']

        auth = OAuthHandler(consumer_key, consumer_secret)

        return tweepy.API(auth)


    def get_tweet_ids(self, term):
        """
        Given a search term or search phrase, find all the IDs of the result
        tweets.
        """
        tweet_ids = []

        refreshCursor = ''

        while True:
            response = self.getJsonReponse(term, refreshCursor)
            refreshCursor = response['min_position']

            try:
                tweets = PyQuery(response['items_html'])('div.js-stream-tweet')
            except Exception:
                break

            #Exit when no more tweets loaded
            if len(tweets) == 0:
                break

            #Don't allow loading more than 100 tweets which is the Twitter API
            #restriction
            if len(tweet_ids) >= 80:
                break

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet_id = tweetPQ.attr("data-tweet-id")
                tweet_ids.append(tweet_id)

        return tweet_ids


    def getJsonReponse(self, term, refreshCursor):
        """
        Prepare HTTP GET request to be sent to Twitter API and search for tweets
        based on given term inside a limited min/max position.
        """
        url = """https://twitter.com/i/search/timeline?f=realtime&q={}&src=typd&max_position={}""".format(urllib.quote(term), refreshCursor)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request).read()
        json_response = json.loads(response)
        return json_response

    def get_tweets(self, term):
        """
        Given a list of tweet IDs, return all information related to it.
        """
        tweet_ids = self.get_tweet_ids(term)

        try:
            tweets = self.api.statuses_lookup(tweet_ids)
        except TweepError:
            return []

        for tweet in tweets:
            tweet_info = self.get_tweet_info(tweet)

        return tweets

    def get_tweet_info(self, tweet):
        """
        Get all the necessary fields required by the rest of the modules:
        text, author, date, geolabels, etc.
        """
        tweet_info = ''
        return tweet_info
