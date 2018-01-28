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
COMBINED_TABLE = 'combinedTable'
COMBINED_TABLE_5_MINUTES = 'combinedTable_5min'

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id = AWS_ACCESS,
                    aws_secret_access_key = AWS_SECRET,
                    region_name = AWS_REGION_NAME)

table_combined = dynamodb.Table(COMBINED_TABLE)
table_combined_5min = dynamodb.Table(COMBINED_TABLE_5_MINUTES)

K = 10

def lambda_handler(event, context):
    try:
        currTime = datetime.now()
        currTime = currTime - timedelta(hours=5)
        newCurrTime = currTime.strftime('%Y-%m-%d-%H-%M')
        currTime = currTime.strftime('%Y-%m-%d-%H-%M-%S')
        response_combined = table_combined.scan(FilterExpression=Attr('key_datetime').lt(currTime))
        
        response_combined_5min = table_combined_5min.scan(FilterExpression=Attr('key_datetime').lt(currTime))
        
        items_combined = response_combined['Items']
        items_total = {}
        for i in items_combined:
            if i['key_word'] not in items_total:
                items_total[i['key_word']] = i['score']
            else:
                items_total[i['key_word']] += i['score']
        topKKeywords = sorted(items_total, key=items_total.get, reverse=True)[:K]
        
        # Delete current entries
        items = response_combined_5min['Items']
        for i in items:
            table_combined_5min.delete_item(
                Key={
                    'key_word': i['key_word']
                })
        
        # Insert new entries
        i = 1
        for keyword in topKKeywords:
            table_combined_5min.put_item(Item= {
                    'key_word' : keyword,
                    'key_datetime' : newCurrTime, 
                    'score' : items_total[keyword],
                    'rank'  : i
                })
            i += 1
        
    except:
        print('Check failed!')
        raise
    else:
        print('Check passed!')
        return "Success"