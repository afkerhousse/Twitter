from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pipeline.twitter_api import generate_bearer_token

def test_generate_bearer_token_success(mock_env_vars):
    mock_response = {
        "access_token": "fake_token"
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        token = generate_bearer_token()
        assert token == "fake_token"

def test_generate_bearer_token_failure(mock_env_vars):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 403
        mock_post.return_value.text = "Forbidden"

        token = generate_bearer_token()
        assert token is None
