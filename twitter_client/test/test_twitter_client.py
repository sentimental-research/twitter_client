import pytest
from TwitterClient import TwitterClient

class TestTwitterClient:

    def test_get_bioconductor_tweets(self):
        term = "#bioconductor"
        # begin = "2006-01-01"
        # end = "2016-03-23"
        client = TwitterClient()
        # results = client.get_tweets(term, begin, end)
        results = client.get_tweets(term)
        assert len(results) < 0
