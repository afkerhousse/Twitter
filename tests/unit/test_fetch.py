from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pipeline.twitter_api import fetch_tweets

def test_fetch_tweets_success(sample_tweet_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_tweet_response

        data = fetch_tweets("test", 10, "fake_token")
        assert "data" in data
        assert len(data["data"]) == 2

def test_fetch_tweets_empty_data():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}

        data = fetch_tweets("none", 10, "fake_token")
        assert data is None

def test_fetch_tweets_rate_limit():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 429
        mock_get.return_value.headers = {"x-rate-limit-reset": "9999999999"}
        mock_get.return_value.text = "Rate limit exceeded"

        data = fetch_tweets("test", 10, "fake_token")
        assert data is None
