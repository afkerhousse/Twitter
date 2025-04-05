import os
import requests
import json
from time import sleep, time
import logging
from dotenv import load_dotenv
import base64
from filelock import FileLock

#Load environment variables from .env file
load_dotenv(override=True)

#Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#Function to generate Bearer Token using X API credentials
def generate_bearer_token():
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")

    if not api_key or not api_secret:
        logging.error("API Key and API Secret are required.")
        raise ValueError("API Key and API Secret are required.")

    #Encode API key and secret for Basic Auth
    credentials = f"{api_key}:{api_secret}".encode("utf-8")
    b64_credentials = base64.b64encode(credentials).decode("utf-8")

    url = "https://api.twitter.com/oauth2/token"
    headers = {
        "Authorization": f"Basic {b64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    data = {"grant_type": "client_credentials"}

    logging.info("Requesting Bearer Token from X API...")
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        bearer_token = response.json().get("access_token")
        logging.info("Bearer Token generated successfully")
        return bearer_token
    else:
        logging.error(f"Error {response.status_code} to get Bearer Token: {response.text}")

#Function to fetch tweets using X API v2
def fetch_tweets(keyword, max_results,  bearer_token, next_token=None): #Set max_results as parameter
    headers = {
        "Authorization": f"Bearer {bearer_token}" #Use Bearer token instead of API key
    }
    
    url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results={max_results}" #Use max_results parameter in URL
    if next_token:
        url += f"&next_token={next_token}"
    
    #Exponential backoff for rate limiting
    for retry in range(5):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logging.info("Request successful")
            #Check if the "data" field exists and has content
            if not response.json().get("data"):
                return None
            else:
                return response.json()

        elif response.status_code == 429:
            #Extract rate limit reset time from headers
            limit_reset = int(response.headers.get("x-rate-limit-reset", time()))
            #Convert unix timestamp into minutes
            current_timestamp = int(time())
            limit_reset_min = (limit_reset - current_timestamp) / 60

            logging.warning(f"Rate limit exceeded. New request allowed in {limit_reset_min} minutes for this endpoint")
            sleep(min(2 ** retry, limit_reset_min * 60)) #Exponential backoff wait time

            #TEST: waiting for limit reset time to test next token -> uncomment below
            #logging.info(f"Sleeping for {limit_reset_min} minutes...")
            #sleep(limit_reset_min * 60 + 5)
            #logging.info("Resuming execution")

        #Add other error handling
        else:
            logging.error(f"Error {response.status_code}: {response.text}")
            return None

    return None

#Function to process tweets 
def process_tweets(data):
    processed_tweets = []

    #Add try-except block to handle KeyError
    try:
        for tweet in data["data"]:
            processed_tweets.append({
                "id": tweet["id"],
                "text": tweet["text"],
                "author_id": tweet.get("author_id", "unknown")
            })
        logging.info(f"Tweets processed successfully ({len(processed_tweets)} tweets)")

    except KeyError as e:
        logging.error(f"KeyError: {e}. Failed to process tweets")

    return processed_tweets

#Function to sav processed tweets to json file
def save_to_file(data, keyword):
    filename = f"tweets_{keyword}.json"
    lock = FileLock(f"{filename}.lock")  #Lock file for synchronization

    #Add try-except block to handle IOError
    try:
        with lock:  #Ensures only one thread writes at a time
            #Check if file already exists and read existing data
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []  # In case of an empty or corrupted file
            else:
                existing_data = []

            #Append new data
            existing_data.extend(data)

            #Write back full valid JSON list
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(existing_data, f)

            logging.info(f"Tweets saved to JSON file successfully ({filename})")

    except Exception as e:
        logging.error(f"Error: {e}. Failed to save tweets to file")

def run_pipeline(keyword="sevdesk", page_max=3, max_results=10):
    logging.info(f'PIPELINE START: keyword="{keyword}", page_max={page_max}, max_results={max_results}')

    bearer_token = generate_bearer_token()

    if not bearer_token:
        logging.error("PIPELINE END: Failed to generate Bearer Token")
        return
    next_token = None
    total_tweets = 0
    for _ in range(page_max):
        logging.info(f"Fetching on page {_+1} for keyword '{keyword}'")
        data = fetch_tweets(keyword, max_results, bearer_token, next_token)

        if not data:
            logging.warning("Exiting piepline: no tweets to process")
            break

        processed_tweets = process_tweets(data)
        total_tweets += len(processed_tweets)

        save_to_file(processed_tweets, keyword)

        #Checking for next_token to fetch next page of tweets
        next_token = data.get("meta", {}).get("next_token", None)
        if not next_token:
            logging.info("Exiting piepline: no more pages to fetch")
            break

    logging.info(f"PIPELINE END: total_tweets={total_tweets}")


### TESTS ###
if __name__ == "__main__":
    run_pipeline(keyword="sevdesk", page_max=3)
    #run_pipeline(keyword="accounting", page_max=3, max_results=20)
    #run_pipeline(keyword="invoice", page_max=2, max_results=10)
    #run_pipeline(keyword="ksedves", page_max=3)