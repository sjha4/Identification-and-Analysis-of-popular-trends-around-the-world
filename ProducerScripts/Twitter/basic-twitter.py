
from TwitterAPI import TwitterAPI
import boto3
import json
import twitterCreds
import AWS_Creds

## twitter credentials

consumer_key = twitterCreds.consumer_key
consumer_secret = twitterCreds.consumer_secret
access_token_key = twitterCreds.access_token_key
access_token_secret = twitterCreds.access_token_secret
aws_acces = AWS_Creds.AWS_ACCESS
aws_secret = AWS_Creds.AWS_SECRET

## Reddit streaming api


api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

kinesis = boto3.client('kinesis', region_name='us-east-1', aws_access_key_id=aws_acces, aws_secret_access_key=aws_secret)

r = api.request('statuses/filter', {'locations':'-90,-90,90,90'})

KEY_DATA = 'data'
KEY_TYPE = 'type'

DATA_TYPE = 'twitter'

tweets = []
count = 0
for item in r:
    jsonItem = json.dumps(item)
    tweets.append({KEY_TYPE = DATA_TYPE, KEY_DATA:jsonItem, 'PartitionKey':"filler"})
    count += 1
    if count == 100:
        kinesis.put_records(StreamName="MeetupTwitterKinesisStream", Records=tweets)
        count = 0
        tweets = []
