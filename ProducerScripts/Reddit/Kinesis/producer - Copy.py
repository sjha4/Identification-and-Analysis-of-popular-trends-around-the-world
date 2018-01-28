#pip install praw

# References:
# 1. Reddit: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#read-only
# 2. AWS: https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
import praw
import boto3
import json

# Reddit credentials
CLIENT_ID =     '38gAflblSmQ8Hg'
CLIENT_SECRET = '51dXwzp-MEmt8x1Zg6qeUM8pucY'
USER_AGENT =    'NCSU/DICProject by Team-8'

# AWS credentials
AWS_SECRET_ACCESS_KEY = 'gjCqXPekb28xV2LH0B4QjKvbLjtkazXloEjDMKXv'
AWS_ACCESS_KEY_ID =     'AKIAJEVOTONJJTMIOZVQ'
AWS_REGION_NAME =       'us-east-1'
AWS_STREAM_NAME =       'MeetupTwitterKinesisStream'

# Reddit Controller
reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = CLIENT_SECRET,
                     user_agent = USER_AGENT)
REDDIT_POST_LIMIT = None
MULTIPLE_POST_SEND_LIMIT = 1000

# Kinesis Controller
kinesis = boto3.client('kinesis',
                        region_name = AWS_REGION_NAME,
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

KEY_TITLE = 'title'
KEY_NUM_COMMENTS = 'nc'
KEY_SCORE = 'score'
KEY_TYPE = 'type'

def getNewRecord():
    return {KEY_TYPE: 'reddit'}

# Fetch the data continuously. Quit on KeyboardInterrupt
try:
    while True:
        data_for_kinesis = []
        for submission in reddit.subreddit('all').new(limit=REDDIT_POST_LIMIT):
            redPost = getNewRecord()
            redPost[KEY_TITLE] = submission.title
            redPost[KEY_NUM_COMMENTS] = submission.num_comments
            redPost[KEY_SCORE] = submission.score
            # data_for_kinesis.append({'Data':json.dumps(redPost), 'PartitionKey':"filler"})
            i = 1
            while i <= MULTIPLE_POST_SEND_LIMIT:
                kinesis.put_record(StreamName = AWS_STREAM_NAME, Data  = json.dumps(redPost), PartitionKey  = "filler")
                i += 1

        for submission in reddit.subreddit('all').controversial(limit=REDDIT_POST_LIMIT):
            redPost = getNewRecord()
            redPost[KEY_TITLE] = submission.title
            redPost[KEY_NUM_COMMENTS] = submission.num_comments
            redPost[KEY_SCORE] = submission.score
            # data_for_kinesis.append({'Data':json.dumps(redPost), 'PartitionKey':"filler"})
            i = 1
            while i <= MULTIPLE_POST_SEND_LIMIT:
                kinesis.put_record(StreamName = AWS_STREAM_NAME, Data  = json.dumps(redPost), PartitionKey  = "filler")
                i += 1

        for submission in reddit.subreddit('all').hot(limit=REDDIT_POST_LIMIT):
            redPost = getNewRecord()
            redPost[KEY_TITLE] = submission.title
            redPost[KEY_NUM_COMMENTS] = submission.num_comments
            redPost[KEY_SCORE] = submission.score
            # data_for_kinesis.append({'Data':json.dumps(redPost), 'PartitionKey':"filler"})
            i = 1
            while i <= MULTIPLE_POST_SEND_LIMIT:
                kinesis.put_record(StreamName = AWS_STREAM_NAME, Data  = json.dumps(redPost), PartitionKey  = "filler")
                i += 1

        for submission in reddit.subreddit('all').rising(limit=REDDIT_POST_LIMIT):
            redPost = getNewRecord()
            redPost[KEY_TITLE] = submission.title
            redPost[KEY_NUM_COMMENTS] = submission.num_comments
            redPost[KEY_SCORE] = submission.score
            # data_for_kinesis.append({'Data':json.dumps(redPost), 'PartitionKey':"filler"})
            i = 1
            while i <= MULTIPLE_POST_SEND_LIMIT:
                kinesis.put_record(StreamName = AWS_STREAM_NAME, Data  = json.dumps(redPost), PartitionKey  = "filler")
                i += 1

        for submission in reddit.subreddit('all').top(limit=REDDIT_POST_LIMIT):
            redPost = getNewRecord()
            redPost[KEY_TITLE] = submission.title
            redPost[KEY_NUM_COMMENTS] = submission.num_comments
            redPost[KEY_SCORE] = submission.score
            # data_for_kinesis.append({'Data':json.dumps(redPost), 'PartitionKey':"filler"})
            i = 1
            while i <= MULTIPLE_POST_SEND_LIMIT:
                kinesis.put_record(StreamName = AWS_STREAM_NAME, Data  = json.dumps(redPost), PartitionKey  = "filler")
                i += 1
        # kinesis.put_records(StreamName = AWS_STREAM_NAME, Records = data_for_kinesis)
except KeyboardInterrupt:
    pass
