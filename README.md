# Research Software Sentiment Analyser 
## Twitter Client

This module is part of the Research Software Sentiment Analyser developed for the Hack Day on the SSI Collaborations Workshop 2016.
It is in charge of querying Twitter and perform an informal search on tweets related to well known libraries used for research software, such as bioconductor or ReciPy.

The input of this module is the search term that is passed to the Twitter API and searches for all tweets in the past that contain a reference to the software, whether it's good or bad. These tweets are then fed into a Sentiment Analyser that automates the analysis of the text and classifies them as negative, positive or neutral reviews. Then this information can be used to create metrics or to elaborate GitHub badges for research software repositories that want to publish the average sentiment of their community of users.

### Usage
To install this module:

```
git clone https://github.com/sentimental-research/twitter_client.git
cd twitter_client
pip install -r requirements.txt
```

In order to connect to Twitter to gather the data, we need a secrets.json file containing your consumer key and secret. You can find the information about how to get this [here](https://apps.twitter.com/), and create a json file in the repo's root directory that looks like this:

```
{
  "consumer_key": "MY_CONSUMER_KEY",
  "consumer_secret": "MY_CONSUMER_SECRET"
}
```



### Test
A reduced number of unit tests have been included. You can run them using py.test:

```
py.test -vv
```

### Ideas for the future

