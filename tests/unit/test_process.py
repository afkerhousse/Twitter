import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pipeline.twitter_api import process_tweets

def test_process_tweets_valid(sample_tweet_response):
    result = process_tweets(sample_tweet_response)
    assert len(result) == 2
    assert result[0]["text"] == "tweet 1"

def test_process_tweets_missing_data():
    data = {"unexpected": []}
    result = process_tweets(data)
    assert result == []
