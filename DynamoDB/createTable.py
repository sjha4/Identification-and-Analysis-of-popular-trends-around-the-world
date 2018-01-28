from __future__ import print_function # Python 2/3 compatibility
import boto3

from AWS_CREDS import *

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

table = dynamodb.create_table(
    TableName='direwolves_101',
    KeySchema=[
        {
            'AttributeName': 'key_hh',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'key_date',
            'KeyType': 'RANGE'  #Sort key
        },
        {
            'AttributeName': 'key_word',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'score',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1250,
        'WriteCapacityUnits': 1250
    }
)

print("Table status:", table.table_status)
