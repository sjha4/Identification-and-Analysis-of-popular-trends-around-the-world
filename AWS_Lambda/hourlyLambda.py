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
COMBINED_TABLE_HOURLY = 'combinedTable_hourly'

dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id = AWS_ACCESS,
                    aws_secret_access_key = AWS_SECRET,
                    region_name = AWS_REGION_NAME)

table_combined = dynamodb.Table(COMBINED_TABLE)
table_combined_hr = dynamodb.Table(COMBINED_TABLE_HOURLY)


def lambda_handler(event, context):
    try:
        currTime = datetime.now()
        currTime = currTime - timedelta(hours=5)
        oldTime = currTime - timedelta(hours=1)
        currTime1 = currTime.strftime('%Y-%m-%d-%H-%M-%S')
        oldTime = oldTime.strftime('%Y-%m-%d-%H-%M-%S')
        newCurrTime = currTime.strftime('%Y-%m-%d-%H')
        #response_combined = table_combined.scan(FilterExpression=Attr('key_datetime').between('2017-11-24-13','2017-11-24-15'))
        response_combined = table_combined.scan(FilterExpression=Attr('key_datetime').between(oldTime,currTime1))
        items_combined = response_combined['Items']
        items_total = {}
        for i in items_combined:
            if i['key_word'] not in items_total:
                items_total[i['key_word']] = i['score']
            else:
                items_total[i['key_word']] += i['score']
            table_combined.delete_item(
                    Key={
                        'key_word': i['key_word'],
                        'key_datetime': i['key_datetime']
                    })
        sorted_by_value = sorted(items_total, key = lambda x: items_total[x], reverse = True)
        for k in items_combined:
            i = 0
            while i < len(sorted_by_value) and i < 10:
                if k['key_word'] == sorted_by_value[i]:
                    print(table_combined_hr.put_item(Item= {
                        'key_word' : k['key_word'],
                        'key_datetime' : newCurrTime, 
                        'score' : k['score'],
                        'rank'  : i + 1
                    }))
                i += 1
    except:
        print('Check failed!')
        raise
    else:
        print('Check passed!')
        return event['time']