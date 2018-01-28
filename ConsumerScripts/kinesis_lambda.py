from __future__ import print_function
from textblob import TextBlob

# See the following links for response packets:
# 1. Reddit: https://github.com/reddit/reddit/wiki/JSON
# 2. Twitter: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
# 3. Meetup: https://www.meetup.com/meetup_api/docs/stream/2/open_events/

import base64
import json
import boto3

print('Loading function')

# ----------- DATA KEYS --------------------------
KEY_TITLE           = 'title'
KEY_NUM_COMMENTS    = 'nc'
KEY_SCORE           = 'score'
KEY_TYPE            = 'type'
KEY_DATA            = 'data'

# ----------- STREAM TYPES ------------------------
REDDIT  = 'reddit'
MEETUP  = 'meetup'
TWITTER = 'twitter'

# ------------ DYNAMO DB CONFIGURATIONS ------------
DYNAMO_DB_REGION_NAME   = ''
DYNAMO_DB_END_POINT     = ''
# These lamdas only put data into the 'live' table.
TWITTER_LIVE_TABLE_NAME = 'live_twitter'
REDDIT_LIVE_TABLE_NAME  = 'live_reddit'
MEETUPS_LIVE_TABLE_NAME = 'live_meetups'

# -------------- HEADER NAMES IN TABLES ------------

# ---------- TWITTER TABLE -------------
TWITTER_TABLE_REPLIES_HEADER     = 'replies'
TWITTER_TABLE_FAVORITES_HEADER   = 'favorites'
TWITTER_TABLE_RETWEETS_HEADER    = 'retweets'

# ---------- REDDIT TABLE --------------
REDDIT_TABLE_SCORE_HEADER           = 'score'
REDDIT_TABLE_NUM_COMMENTS_HEADER    = 'num_comments'

# ---------- MEETUPS TABLE -------------
MEETUPS_LOCATION_KEY_HEADER     = 'location'
MEETUPS_TABLE_CATEGORY_HEADER   = 'category'
MEETUPS_TABLE_VENUE_HEADER      = 'venue'
MEETUPS_TABLE_NAME_HEADER       = 'name'

# ---------- COMMON HEADERS ------------
TIME_HEADER = 'time'
KEYWORD_HEADER = 'keyword'


dynamodb = boto3.resource('dynamodb', region_name = DYNAMO_DB_REGION_NAME, endpoint_url=DYNAMO_DB_END_POINT)

def extract_keywords(sentence):
    """
        Extracts Noun Phrases. Has an external dependency on textblob.
    """
    keywords = []
    blob = TextBlob(sentence)
    for np in blob.noun_phrases:
        keywords.append(np)
    return keywords

def getTimeKey():
    return str(datetime.datetime.now().time().strftime("%H"))

def updateFieldInTable(table, fieldName, fieldValue, timeKey, keywords):
    for keyword in keywords:
        table.update_item(
            Key = {
                TIME_HEADER: timeKey,
                KEYWORD_HEADER: keyword
            },
            UpdateExpression="set " + fieldName + " = " + fieldName + " + :val",
            ExpressionAttributeValues={
                ':val': decimal.Decimal(fieldValue)
            },
            ReturnValues="UPDATED_NEW"
        )

def lambda_handler(event, context):
    output = {}

    for record in event['records']:
        data = json.loads(base64.b64decode(record['data']))

        print("Record: " + record)
        timeKey = getTimeKey()

        if data[KEY_TYPE] == REDDIT:
            # Find keywords from the title.
            title = data[KEY_DATA]['title']
            keywords = extract_keywords(title)

            # Extract score and number of comments.
            score = data[KEY_DATA]['score']
            num_comments = data[KEY_DATA]['num_comments']

            # Put these into Dynamo
            table =  dynamodb.Table(REDDIT_LIVE_TABLE_NAME)

            updateFieldInTable(table, REDDIT_TABLE_NUM_COMMENTS_HEADER, num_comments, timeKey, keywords)
            updateFieldInTable(table, REDDIT_TABLE_SCORE_HEADER, score, timeKey, keywords)
        elif data[KEY_TYPE] == MEETUP:
            # Find keywords from the name.
            event_name = data[KEY_DATA]['name']
            keywords   = extract_keywords(event_name)

            # Extract venue
            # NOTE: May not be present
            cityStateCountry = {}
            venue = {}
            if 'venue' in data[KEY_DATA]:
                cityStateCountry['city']        = data[KEY_DATA]['venue']['city']
                cityStateCountry['country']     = data[KEY_DATA]['venue']['country']
                if 'state' in data[KEY_DATA]['venue']:
                    cityStateCountry['state']   = data[KEY_DATA]['venue']['state']
                venue['name']           = data[KEY_DATA]['venue']['name']
                if 'address_1' in data[KEY_DATA]['venue']:
                    venue['address_1']  = data[KEY_DATA]['venue']['address_1']
                if 'address_2' in data[KEY_DATA]['venue']:
                    venue['address_2']  = data[KEY_DATA]['venue']['address_2']
                if 'address_3' in data[KEY_DATA]['venue']:
                    venue['address_3']  = data[KEY_DATA]['venue']['address_3']
            else:
                # If not present, assume the venue to be in the group's location.
                venue = {}
                cityStateCountry['city']        = data[KEY_DATA]['group']['city']
                cityStateCountry['country']     = data[KEY_DATA]['group']['country']
                if 'state' in data[KEY_DATA]['group']:
                    cityStateCountry['state']   = data[KEY_DATA]['group']['state']

            # Extract category
            event_category = data[KEY_DATA]['group']['category']

            # Put these into Dynamo
            table =  dynamodb.Table(MEETUPS_LIVE_TABLE_NAME)
            for keyword in keywords:
                table.put_item(
                    Item={
                            TIME_HEADER:     timeKey,                           # Part of key. To filter on time.
                            KEYWORD_HEADER:  keyword,                           # Part of key. ?
                            MEETUPS_LOCATION_KEY_HEADER: cityStateCountry,      # Part of key. To filter on geography.
                            MEETUPS_TABLE_CATEGORY_HEADER: event_category,      # Could be part of key. Will allow searching for popular meetups according to category.
                            MEETUPS_TABLE_NAME_HEADER:     event_name,          # Could be part of key. Will allow searching for particular events and find where therey are popular.
                            MEETUPS_TABLE_VENUE_HEADER:    venue                # Could be part of key. Will allow searching for popular events at a venue.
                        }
                    )
        elif data[KEY_TYPE] == TWITTER:
            # Find keywords from the title.
            title       = data[KEY_DATA]['text']
            keywords    = extract_keywords(title)

            # Extract number of retweets, favorites, and replies.
            retweets    = data[KEY_DATA]['retweet_count']
            favorites   = data[KEY_DATA]['favorite_count']
            replies     = data[KEY_DATA]['reply_count']

            # Put these into Dynamo.
            table       = dynamodb.Table(REDDIT_LIVE_TABLE_NAME)

            updateFieldInTable(table, TWITTER_TABLE_RETWEETS_HEADER, retweets, timeKey, keywords)
            updateFieldInTable(table, TWITTER_TABLE_FAVORITES_HEADER, favorites, timeKey, keywords)
            updateFieldInTable(table, TWITTER_TABLE_REPLIES_HEADER, replies, timeKey, keywords)
        else:
            print ("Invalid data type!")

    print('Successfully processed {} records.'.format(len(event['records'])))

    # return {'records': output}
