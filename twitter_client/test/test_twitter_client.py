import pytest
from TwitterClient import TwitterClient

class TestTwitterClient:

    def test_get_bioconductor_tweets(self):
        term = "#bioconductor"
        client = TwitterClient()
        results = client.get_tweets(term)
        assert len(results) == 82

    def test_get_empty_tweets(self):
        term = "#mnhgjkugfdvgh9458345"
        client = TwitterClient()
        results = client.get_tweets(term)
        assert len(results) == 0
