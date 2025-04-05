# Debugging a Faulty Twitter API v2 ETL Pipeline 

### Expected outcome 
After fixing the pipeline, it should: 
- Fetch tweets using the Twitter API v2 with proper authentication. 
- Handle rate-limiting and pagination correctly. 
- Validate API responses and process only valid data. 
- Write the results to a JSON file without corruption, even in multi-threaded environments. 
- Log meaningful progress and error information. 

***

### Approach and debugging strategy
1. **Review resources**: instructions, existing codebase, Twitter API documentation
2. **Environment setup**: Python virtual environment, GitHub repo, Twitter API credentials in .env
3. **Sanity check**: Test API calls manually to understand the response and rate limits
4. **Plan**: Create a checklist of identified issues, bugs to fix, improvement to add
5. **Test**: Run pipelines for various keywords and analyze results

### Fixes and improvements
✅ Replaced static API key auth with dynamic bearer token generation  
✅ Stored sensitive credentials securely in .env (for local run, otherwise a Secret Manager would be the best solution)  
✅ Extracted logic for handling rate limits using exponential backoff and retry mechanism  
✅ Added proper error handling for unexpected status codes or other exceptions through the script  
✅ Added logging for better observability and troubleshooting  
✅ Used FileLock to safely write to JSON in a multi-threaded scenario  
✅ Prevented JSON corruption by reading + rewriting the file instead of appending  
✅ Added flexibility by making max_results, page_max, and keyword configurable  
✅ Ensured exits when no tweets are returned or token fails  

### Sample test results
**TEST 1: keyword="sevdesk", page_max=3, max_results=10**  
Expected:
2 tweets in file tweets_sevdesk.json  
Pipeline satus: 1/1 page, complete

    2025-04-05 16:52:37,939 - INFO - PIPELINE START: keyword="sevdesk", page_max=3, max_results=10
    2025-04-05 16:52:37,939 - INFO - Requesting Bearer Token from X API...
    2025-04-05 16:52:38,340 - INFO - Bearer Token generated successfully
    2025-04-05 16:52:38,340 - INFO - Fetching on page 1 for keyword 'sevdesk'
    2025-04-05 16:52:38,614 - INFO - Request successful
    2025-04-05 16:52:38,614 - INFO - Tweets processed successfully (2 tweets)
    2025-04-05 16:52:38,622 - INFO - Tweets saved to JSON file successfully (tweets_sevdesk.json)
    2025-04-05 16:52:38,626 - INFO - Exiting piepline: no more pages to fetch
    2025-04-05 16:52:38,626 - INFO - PIPELINE END: Total total_tweets=2

**TEST 2: keyword="accounting", page_max=3, max_results=20**  
Expected: 20 tweets in file tweets_accounting.json  
Pipeline satus: 1/3 page, exited because of rate limit

    2025-04-04 16:10:54,271 - INFO - PIPELINE START: keyword="accounting", page_max=3, max_results=20
    2025-04-04 16:10:54,272 - INFO - Requesting Bearer Token from X API...
    2025-04-04 16:10:54,628 - INFO - Bearer Token generated successfully
    2025-04-04 16:10:54,977 - INFO - Fetching on page 1 for keyword 'accounting'
    2025-04-04 16:10:54,978 - INFO - Request successful
    2025-04-04 16:10:54,978 - INFO - Tweets processed successfully (20 tweets)
    2025-04-04 16:10:54,982 - INFO - Tweets saved to JSON file successfully (tweets_accounting.json)
    2025-04-04 16:10:54,983 - INFO - Fetching on page 2 for keyword 'accounting'
    2025-04-04 16:10:55,176 - WARNING - Rate limit exceeded. New request allowed in 15.0 minutes for this endpoint
    2025-04-04 16:10:56,381 - WARNING - Rate limit exceeded. New request allowed in 14.983333333333333 minutes for this endpoint
    2025-04-04 16:10:58,603 - WARNING - Rate limit exceeded. New request allowed in 14.95 minutes for this endpoint
    2025-04-04 16:11:02,830 - WARNING - Rate limit exceeded. New request allowed in 14.883333333333333 minutes for this endpoint
    2025-04-04 16:11:11,055 - WARNING - Rate limit exceeded. New request allowed in 14.733333333333333 minutes for this endpoint
    2025-04-04 16:11:27,056 - WARNING - Exiting piepline: no tweets to process
    2025-04-04 16:11:27,059 - INFO - PIPELINE END: total_tweets=20 

**TEST 3: keyword="invoice", page_max=2, max_results=10**  
Expected: 20 tweets expected in tweets_invoice.json  
Pipeline satus: 2/2 pages, complete after waiting 15min reset limit 

    2025-04-04 16:43:48,728 - INFO - PIPELINE START: keyword="invoice", page_max=2, max_results=10
    2025-04-04 16:43:48,728 - INFO - Requesting Bearer Token from X API...
    2025-04-04 16:43:49,043 - INFO - Bearer Token generated successfully
    2025-04-04 16:43:49,333 - INFO - Fetching on page 1 for keyword 'invoice'
    2025-04-04 16:43:49,334 - INFO - Request successful
    2025-04-04 16:43:49,334 - INFO - Tweets processed successfully (10 tweets)
    2025-04-04 16:43:49,338 - INFO - Tweets saved to JSON file successfully (tweets_invoice.json)
    2025-04-04 16:43:49,339 - INFO - Fetching on page 2 for keyword 'invoice'
    2025-04-04 16:43:49,623 - WARNING - Rate limit exceeded. New request allowed in 15.0 minutes for this endpoint
    2025-04-04 16:43:49,623 - INFO - Sleeping for 15.0 minutes...
    2025-04-04 16:58:54,654 - INFO - Resuming execution
    2025-04-04 16:58:55,091 - INFO - Request successful
    2025-04-04 16:58:55,091 - INFO - Tweets processed successfully (10 tweets)
    2025-04-04 16:58:55,097 - INFO - Tweets saved to JSON file successfully (tweets_invoice.json)
    2025-04-04 16:58:55,100 - INFO - PIPELINE END: total_tweets=20 

**TEST 4: keyword="ksedves", page_max=3, max_results=10**  
Expected: no tweets, no file
Pipeline satus: 0 page, complete because no data

    2025-04-05 17:42:33,024 - INFO - PIPELINE START: keyword="ksedves", page_max=3, max_results=10
    2025-04-05 17:42:33,026 - INFO - Requesting Bearer Token from X API...
    2025-04-05 17:42:33,376 - INFO - Bearer Token generated successfully
    2025-04-05 17:42:33,376 - INFO - Fetching on page 1 for keyword 'ksedves'
    2025-04-05 17:42:33,706 - INFO - Request successful
    2025-04-05 17:42:33,706 - WARNING - Exiting piepline: no tweets to process
    2025-04-05 17:42:33,706 - INFO - PIPELINE END: total_tweets=0

**TEST 5: Invalid API credentials**  
Expected: logged error when requesting bearer token  
Pipeline status: raise error

    2025-04-05 18:04:27,804 - INFO - PIPELINE START: keyword="sevdesk", page_max=3, max_results=10
    2025-04-05 18:04:27,804 - INFO - Requesting Bearer Token from X API...
    2025-04-05 18:04:28,196 - ERROR - Error 403 to get Bearer Token: {"errors":[{"code":99,"message":"Unable to verify your credentials","label":"authenticity_token_error"}]}
    2025-04-05 18:04:28,196 - ERROR - PIPELINE END: Failed to generate Bearer Token

### Possible enhancements
- Unit tests (uing pytest for instance)
- Filter only new tweets for one keyword to avoid duplicates (filter by id)
- 