# pip install praw
# Reference: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#read-only

import boto3
import json
import praw
import redditCreds

reddit = praw.Reddit(client_id=redditCreds.client_id,
                     client_secret=redditCreds.client_secret,
                     user_agent=redditCreds.user_agent)
try:
    while True:
        for submission in reddit.subreddit('all').new(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').controversial(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').gilded(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').hot(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').new(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').rising(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').top(limit=None):
            try: print submission.title
            except: pass
except KeyboardInterrupt:
    pass
