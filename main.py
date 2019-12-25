import json
import praw
import pandas as pd

url = 'https://www.reddit.com/'
with open('credentials.json') as f:
    params = json.load(f)

reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['api_key'],
                     password=params['password'],
                     user_agent='Test App for pulling saved comments accessAPI:v0.0.1 (by /u/priya90r)',
                     username=params['username'])

s = reddit.redditor(params['username']).saved(limit=None)

posts = []
i = 0

for post in s:
    try:
        i += 1
        posts.append(
            [post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    except AttributeError as err:
        print(err)
    if i % 5 == 0:
        print(f'{i} submissions completed')
saved_df = pd.DataFrame(posts, columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

saved_df.to_csv("20191225_saved_comments_{}.csv".format(params['username']))
