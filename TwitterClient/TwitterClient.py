import urllib, urllib2, json, tweepy, csv
from pyquery import PyQuery
from tweepy import OAuthHandler
from tweepy.error import TweepError

__all__ = ['TwitterClient']

class TwitterClient(object):
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

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet_id = tweetPQ.attr("data-tweet-id")
                tweet_ids.append(tweet_id)

            if len(tweet_ids) > 700:
                break

        return tweet_ids


    def getJsonReponse(self, term, refreshCursor):
        """
        Prepare HTTP GET request to be sent to Twitter API and search for tweets
        based on given term inside a limited min/max position.
        """
        url = """https://twitter.com/i/search/timeline?f=realtime&q={}&src=typd&max_position={}""".format(urllib.quote(term), refreshCursor)
        print url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        request = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(request).read()
        json_response = json.loads(response)
        return json_response

    def slice_list(self, input_list, size):
       "Slice an input list into a specific size and yield shorten lists"
       for i in range(0, len(input_list), size):
           yield input_list[i:i + size]
       return

    def get_tweets(self, term):
        """
        Given a list of tweet IDs, return all information related to it.
        """
        tweet_ids = self.get_tweet_ids(term)
        tweets = []

        # try:
        for tweet in self.query_api(tweet_ids):
            tweets.append(self.get_tweet_info(tweet))
        # except TweepError:
        #     return tweets

        return tweets

    def query_api(self, tweet_ids):
        """
        """
        print "tweet_ids " + str(len(tweet_ids))
        for hundred_tweets in self.slice_list(tweet_ids, 100):
            print hundred_tweets
            for tweet in self.api.statuses_lookup(hundred_tweets):
                yield tweet

    def get_tweet_info(self, tweet):
        """
        Get all the necessary fields required by the rest of the modules:
        text, author, date, geolabels, etc.
        """
        tweet_info = {}

        tweet_info['username'] = tweet.author.screen_name
        tweet_info['date'] = tweet.created_at
        tweet_info['text'] = self.text_format(tweet.text)
        tweet_info['id'] = tweet.id

        return tweet_info

    def text_format(self, text):
        text = text.encode('utf-8')
        text = text.replace('"',' ').replace("\n"," ")
        return text

    def write_results(self, tweets):
        """
        Save results in an output csv file.
        """
        headers = ['username','date','text','id']
        with open('tweets.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, headers)
            writer.writeheader()
            for tweet in tweets:
                writer.writerow(tweet)
