from __future__ import print_function

import os
from datetime import datetime
from urllib2 import urlopen
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
from time import gmtime, strftime
from datetime import datetime, timedelta

AWS_ACCESS = os.environ['AWS_ACCESS']  # URL of the site to check, stored in the site environment variable, e.g. https://aws.amazon.com
AWS_SECRET = os.environ['AWS_SECRET']  # String expected to be on the page, stored in the expected environment variable, e.g. Amazon
AWS_STREAM_NAME = os.environ['AWS_STREAM_NAME']
AWS_REGION_NAME = os.environ['AWS_REGION_NAME']
TWITTER_LIVE_TABLE_NAME = 'live_twitter_dic8'
REDDIT_LIVE_TABLE_NAME  = 'live_reddit_dic8'
COMBINED_TABLE = 'combinedTable'

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id = AWS_ACCESS,
                    aws_secret_access_key = AWS_SECRET,
                    region_name = AWS_REGION_NAME)

table_reddit =  dynamodb.Table(REDDIT_LIVE_TABLE_NAME)
table_twitter = dynamodb.Table(TWITTER_LIVE_TABLE_NAME)
table_combined = dynamodb.Table(COMBINED_TABLE)


def lambda_handler(event, context):
    try:
        currTime = datetime.now()
        currTime = currTime - timedelta(hours=5)
        oldTime = currTime - timedelta(minutes=1)
        currTime = str(currTime.strftime('%Y-%m-%d-%H-%M-%S'))
        oldTime = str(oldTime.strftime('%Y-%m-%d-%H-%M-%S'))
        #response_reddit = table_reddit.scan(FilterExpression=Attr('key_datetime').between('2017-11-24-00-00-00','2017-11-24-23-59-59'))
        #response_reddit = table_reddit.scan(FilterExpression=Attr('key_datetime').between(oldTime,currTime))
        #response_reddit = table_reddit.scan(FilterExpression=Attr('key_datetime').between(oldTime,currTime))
        response_reddit = table_reddit.scan(FilterExpression=Attr('key_datetime').lt(currTime))
        print(response_reddit)
        items_reddit = response_reddit['Items']
        for i in items_reddit:
            if 'score' in i and 'num_comments' in i:
                score = int(0.2 * float(i['num_comments']) + 0.8 * float(i['score']))
                print(table_combined.put_item(Item= {
                    'key_word' : i['key_word'],
                    'key_datetime' : i['key_datetime'], 
                    'score' : Decimal(score)}))
                table_reddit.delete_item(
                    Key={
                        'key_word': i['key_word'],
                        'key_datetime': i['key_datetime']
                    })
            else:
                print(table_combined.put_item(Item= {
                    'key_word' : i['key_word'],
                    'key_datetime' : i['key_datetime'], 
                    'score' : Decimal(0)}))
                table_reddit.delete_item(
                    Key={
                        'key_word': i['key_word'],
                        'key_datetime': i['key_datetime']
                    })
        
        #response_twitter = table_twitter.scan(FilterExpression=Attr('key_datetime').between('2017-11-24-14-57-32','2017-11-24-14-57-37'))
        # response_twitter = table_twitter.scan(FilterExpression=Attr('key_datetime').between(oldTime,currTime))
        response_twitter = table_twitter.scan(FilterExpression=Attr('key_datetime').lt(currTime))
        items_twitter = response_twitter['Items']
        for i in items_twitter:
            if 'replies' in i and 'retweets' in i and 'favorites' in i:
                score = int(0.2 * float(i['replies']) + 0.5 * float(i['retweets']) + 0.3 *float(i['favorites']) )
                print(table_combined.put_item(Item= {
                    'key_word' : i['key_word'],
                    'key_datetime' : i['key_datetime'], 
                    'score' : Decimal(score)}))
                table_twitter.delete_item(
                    Key={
                        'key_word': i['key_word'],
                        'key_datetime': i['key_datetime']
                    })
            else:
                print(table_combined.put_item(Item= {
                    'key_word' : i['key_word'],
                    'key_datetime' : i['key_datetime'], 
                    'score' : Decimal(0)}))
                table_twitter.delete_item(
                    Key={
                        'key_word': i['key_word'],
                        'key_datetime': i['key_datetime']
                    })
    except:
        print('Check failed!')
        raise
    else:
        print('Check passed!')
        return event['time']