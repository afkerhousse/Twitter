Exercise: Debugging a Faulty Twitter API v1 ETL Pipeline 
Objective 
Your task is to debug and fix the provided Python ETL pipeline that interacts with the Twitter API v2. The pipeline fetches recent tweets based on a keyword, processes the data, and writes the results to a JSON file. The code is intentionally flawed to test your problem-solving and debugging skills. 
Expected Outcome 
After fixing the pipeline, it should: 
•	Fetch tweets using the Twitter API v2 with proper authentication. 
•	Handle rate-limiting and pagination correctly. 
•	Validate API responses and process only valid data. 
•	Write the results to a JSON file without corruption, even in multi-threaded environments. 
•	Log meaningful progress and error information. 
________________________________________
Steps:
-	Inspect codebase
-	Sign up on X developer portal
-	Get API credentials
-	Explore API collection with Postman, find used endpoint and test connection with API creds (used bearer token generated from twitter developer portal)
-	List errors + fix “obvious” ones
-	Add logging info for progress and errors
-	Setup virtual env + add API creds in .env file
-	Tests: 
o	Keyword=sevdesk, page_max=3, max_results=10
o	Keyword=accounting, page_max=3, max_results=20
o	Keyword=invoice, page_max=2, max_results=30
o	
Errors list:
-	Added max result as param in func fetch tweet, change default to 10 since it is the min value for the param max_results
-	Change api key to bearer according to API auth 
o	Dynamically generate new token, ensure validity in case it get revoked 
o	Security: not save in .env
o	Better scalability for multi-user application (not static and hardcoded + several bearer per user)
o	
-	q
2025-04-04 15:41:30,580 - INFO - RUNNING PIPELINE: fetching 3 pages max of tweets for keyword 'sevdesk'
2025-04-04 15:41:30,581 - INFO - Requesting Bearer Token from X API...
2025-04-04 15:41:30,901 - INFO - Bearer Token generated successfully
2025-04-04 15:41:31,120 - WARNING - Rate limit exceeded. New request allowed in 0.26666666666666666 minutes for this endpoint
2025-04-04 15:41:32,343 - WARNING - Rate limit exceeded. New request allowed in 0.25 minutes for this endpoint
2025-04-04 15:41:34,555 - WARNING - Rate limit exceeded. New request allowed in 0.21666666666666667 minutes for this endpoint
2025-04-04 15:41:38,784 - WARNING - Rate limit exceeded. New request allowed in 0.15 minutes for this endpoint
2025-04-04 15:41:47,089 - INFO - Request successful
2025-04-04 15:41:47,089 - INFO - Tweets processed successfully (2 tweets)
2025-04-04 15:41:47,090 - INFO - Fetched 2 tweets on page 1
2025-04-04 15:41:47,090 - INFO - No more pages to fetch
2025-04-04 15:41:47,091 - INFO - Tweets processed successfully



2025-04-04 16:10:54,271 - INFO - PIPELINE START: fetching 3 pages max of tweets for keyword 'accounting'
2025-04-04 16:10:54,272 - INFO - Requesting Bearer Token from X API...
2025-04-04 16:10:54,628 - INFO - Bearer Token generated successfully
2025-04-04 16:10:54,977 - INFO - Request successful
2025-04-04 16:10:54,978 - INFO - Tweets processed successfully (20 tweets)
2025-04-04 16:10:54,978 - INFO - 20 tweets on page 1
2025-04-04 16:10:55,176 - WARNING - Rate limit exceeded. New request allowed in 15.0 minutes for this endpoint
2025-04-04 16:10:56,381 - WARNING - Rate limit exceeded. New request allowed in 14.983333333333333 minutes for this endpoint
2025-04-04 16:10:58,603 - WARNING - Rate limit exceeded. New request allowed in 14.95 minutes for this endpoint
2025-04-04 16:11:02,830 - WARNING - Rate limit exceeded. New request allowed in 14.883333333333333 minutes for this endpoint
2025-04-04 16:11:11,055 - WARNING - Rate limit exceeded. New request allowed in 14.733333333333333 minutes for this endpoint
2025-04-04 16:11:27,056 - ERROR - No tweets to process
2025-04-04 16:11:27,056 - INFO - 0 tweets on page 2
2025-04-04 16:11:27,058 - ERROR - No data returned from API
2025-04-04 16:11:27,059 - INFO - Tweets saved to JSON file successfully (040425_161127_tweets_accounting.json)
2025-04-04 16:11:27,059 - INFO - PIPELINE END: Total tweets fetched: 20 


2025-04-04 16:43:48,728 - INFO - PIPELINE START: fetching 2 pages max of tweets for keyword 'invoice'
2025-04-04 16:43:48,728 - INFO - Requesting Bearer Token from X API...
2025-04-04 16:43:49,043 - INFO - Bearer Token generated successfully
2025-04-04 16:43:49,333 - INFO - Request successful
2025-04-04 16:43:49,334 - INFO - Tweets processed successfully (10 tweets)
2025-04-04 16:43:49,334 - INFO - 10 tweets on page 1
2025-04-04 16:43:49,338 - INFO - Tweets saved to JSON file successfully (tweets_invoice.json)
2025-04-04 16:43:49,623 - WARNING - Rate limit exceeded. New request allowed in 15.0 minutes for this endpoint
2025-04-04 16:43:49,623 - INFO - Sleeping for 15.0 minutes...
2025-04-04 16:58:54,654 - INFO - Resuming execution
2025-04-04 16:58:55,090 - INFO - Request successful
2025-04-04 16:58:55,091 - INFO - Tweets processed successfully (10 tweets)
2025-04-04 16:58:55,091 - INFO - 10 tweets on page 2
2025-04-04 16:58:55,097 - INFO - Tweets saved to JSON file successfully (tweets_invoice.json)
2025-04-04 16:58:55,100 - INFO - PIPELINE END: Total tweets fetched: 20 
