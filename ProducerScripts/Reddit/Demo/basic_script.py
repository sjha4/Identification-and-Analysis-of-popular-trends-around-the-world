#pip install praw
# Reference: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#read-only

import praw

reddit = praw.Reddit(client_id='38gAflblSmQ8Hg',
                     client_secret='51dXwzp-MEmt8x1Zg6qeUM8pucY',
                     user_agent='NCSU?DICProject by Team-8')
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

        for submission in reddit.subreddit('all').rising(limit=None):
            try: print submission.title
            except: pass

        for submission in reddit.subreddit('all').top(limit=None):
            try: print submission.title
            except: pass
except KeyboardInterrupt:
    pass
