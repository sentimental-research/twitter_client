import pytest
from TwitterClient import TwitterClient

class TestTwitterClient:

    def test_get_bioconductor_tweets(self):
        """
        Check if we get the expected results for bioconductor.
        """
        term = "#bioconductor"
        client = TwitterClient()
        results = client.get_tweets(term)
        assert len(results) == 82

    def test_get_recipy_tweets(self):
        """
        Check if we get the expected behaviour when very few tweets returned.
        """
        term = "#recipy"
        client = TwitterClient()
        results = client.get_tweets(term)
        assert len(results) == 0

    def test_get_empty_tweets(self):
        """
        Check if we get the expected behaviour when no tweets are returned.
        """
        term = "#mnhgjkugfdvgh9458345"
        client = TwitterClient()
        results = client.get_tweets(term)
        assert len(results) == 0
