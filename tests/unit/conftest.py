import pytest
from unittest.mock import patch

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("X_API_KEY", "fake_api_key")
    monkeypatch.setenv("X_API_SECRET", "fake_api_secret")

@pytest.fixture
def sample_tweet_response():
    return {
        "data": [
            {"id": "1", "text": "tweet 1", "author_id": "123"},
            {"id": "2", "text": "tweet 2", "author_id": "456"}
        ],
        "meta": {
            "next_token": "token123"
        }
    }
