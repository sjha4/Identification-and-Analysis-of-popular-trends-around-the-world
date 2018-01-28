#pip install praw

# References:
# 1. Reddit: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#read-only
# 2. AWS: https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
import praw, sys
from AWS_CREDS import *

# Reddit credentials
CLIENT_ID       =     '38gAflblSmQ8Hg'
CLIENT_SECRET   =     '51dXwzp-MEmt8x1Zg6qeUM8pucY'
USER_AGENT      =     'NCSU/DICProject by Team-8'

# Reddit Controller
reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = CLIENT_SECRET,
                     user_agent = USER_AGENT)

REDDIT_POST_LIMIT = None
MULTIPLE_POST_SEND_LIMIT = 1000
if len(sys.argv) == 2:
    MULTIPLE_POST_SEND_LIMIT = int(sys.argv[1])
KINESIS_PUT_BATCH_SIZE = MULTIPLE_POST_SEND_LIMIT / 10

KINESIS_PUT_BATCH_SIZE = 1 if KINESIS_PUT_BATCH_SIZE == 0 else KINESIS_PUT_BATCH_SIZE
KINESIS_PUT_BATCH_SIZE = 500 if KINESIS_PUT_BATCH_SIZE > 500 else KINESIS_PUT_BATCH_SIZE

# Fetch the data continuously. Quit on KeyboardInterrupt
try:
    while True:
        try:
            for data in reddit.subreddit('all').new(limit=REDDIT_POST_LIMIT):
                putDataToKinesisStream(data, TYPE_REDDIT, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)

            for data in reddit.subreddit('all').controversial(limit=REDDIT_POST_LIMIT):
                putDataToKinesisStream(data, TYPE_REDDIT, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)

            for data in reddit.subreddit('all').hot(limit=REDDIT_POST_LIMIT):
                putDataToKinesisStream(data, TYPE_REDDIT, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)

            for data in reddit.subreddit('all').rising(limit=REDDIT_POST_LIMIT):
                putDataToKinesisStream(data, TYPE_REDDIT, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)

            for data in reddit.subreddit('all').top(limit=REDDIT_POST_LIMIT):
                putDataToKinesisStream(data, TYPE_REDDIT, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)
        except KeyboardInterrupt:
            break
        except:
            pass
