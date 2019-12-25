import json
import praw

url = 'https://www.reddit.com/'
with open('credentials.json') as f:
    params = json.load(f)

reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['api_key'],
                     password=params['password'],
                     user_agent='Test App for pulling saved comments accessAPI:v0.0.1 (by /u/priya90r)',
                     username=params['username'])

subreddit = reddit.subreddit('machinelearning')
print(subreddit.display_name)
print(subreddit.title)
print(subreddit.description)