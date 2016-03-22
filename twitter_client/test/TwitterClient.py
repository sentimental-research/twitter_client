import urllib, urllib2, json
from pyquery import PyQuery

class TwitterClient:

    def get_tweets(self, term):

        tweet_ids = []

        refreshCursor = ''

        while True:
            response = self.getJsonReponse(term, refreshCursor)
            refreshCursor = response['min_position']
            tweets = PyQuery(response['items_html'])('div.js-stream-tweet')

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet_id = tweetPQ.attr("data-tweet-id")
                tweet_ids.append(tweet_id)

            break






        return tweet_ids


    def getJsonReponse(self, term, refreshCursor):
        url = "https://twitter.com/i/search/timeline?f=realtime&q={}&src=typd&max_position={}".format(urllib.quote(term), refreshCursor)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        # print "URL: " + url
        request = urllib2.Request(url, headers = headers)
        jsonResponse = urllib2.urlopen(request).read()
        dataJson = json.loads(jsonResponse)
        return dataJson
