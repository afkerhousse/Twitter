import os
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from pipeline.twitter_api import save_to_file

def test_save_to_file(tmp_path):
    tweets = [{"id": "1", "text": "Tweet text", "author_id": "42"}]
    filename = tmp_path / "tweets_test.json"

    # Change working dir to temp
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    save_to_file(tweets, "test")

    with open("tweets_test.json", "r", encoding="utf-8") as f:
        saved = json.load(f)

    assert saved == tweets

    os.chdir(original_cwd)
