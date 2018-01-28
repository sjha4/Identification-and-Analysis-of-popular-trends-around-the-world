import boto3, base64, datetime
import json, time
from textblob import TextBlob

from multiprocessing import Process

from AWS_CREDS import *

def consumer(shard_id):
    kinesis = boto3.client('kinesis',
                            region_name = AWS_REGION_NAME,
                            aws_access_key_id = AWS_ACCESS_KEY_ID,
                            aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

    # Shard iterator
    shard_it = kinesis.get_shard_iterator(StreamName=AWS_STREAM_NAME, ShardId=shard_id, \
        ShardIteratorType="LATEST")["ShardIterator"]

    # ----------- DATA KEYS --------------------------
    KEY_TITLE           = 'title'
    KEY_NUM_COMMENTS    = 'nc'
    KEY_SCORE           = 'score'
    KEY_TYPE            = 'type'
    KEY_DATA            = 'Data'

    # ----------- STREAM TYPES ------------------------
    REDDIT  = 'reddit'
    MEETUP  = 'meetup'
    TWITTER = 'twitter'

    # These lamdas only put data into the 'live' table.
    TWITTER_LIVE_TABLE_NAME = 'live_twitter_dic8'
    REDDIT_LIVE_TABLE_NAME  = 'live_reddit_dic8'
    MEETUPS_TABLE_NAME = 'meetups_dic8'

    # -------------- HEADER NAMES IN TABLES ------------

    # ---------- TWITTER TABLE -------------
    TWITTER_TABLE_REPLIES_HEADER     = 'replies'
    TWITTER_TABLE_FAVORITES_HEADER   = 'favorites'
    TWITTER_TABLE_RETWEETS_HEADER    = 'retweets'

    # ---------- REDDIT TABLE --------------
    REDDIT_TABLE_SCORE_HEADER           = 'score'
    REDDIT_TABLE_NUM_COMMENTS_HEADER    = 'num_comments'

    # ---------- MEETUPS TABLE -------------
    MEETUPS_LOCATION_CITY_KEY_HEADER        = 'key_location_city'
    MEETUPS_LOCATION_STATE_KEY_HEADER       = 'key_location_state'
    MEETUPS_LOCATION_COUNTRY_KEY_HEADER     = 'key_location_country'
    MEETUPS_TABLE_CATEGORY_HEADER   = 'key_category'
    MEETUPS_TABLE_VENUE_HEADER      = 'venue'
    MEETUPS_TABLE_NAME_HEADER       = 'name'

    # ---------- COMMON HEADERS ------------
    TIME_HEADER = 'key_datetime'
    KEYWORD_HEADER = 'key_word'


    dynamodb = boto3.resource('dynamodb',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                        region_name = DYNAMO_DB_REGION_NAME)

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
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

    def updateFieldInTable(table, fieldName, fieldValue, timeKey, keywords):
        # print keywords
        for keyword in keywords:
            table.update_item(
                Key = {
                    TIME_HEADER: timeKey,
                    KEYWORD_HEADER: keyword
                },
                UpdateExpression="set " + fieldName + " = if_not_exists(" + fieldName + ", :init) + :val",
                ExpressionAttributeValues={
                    ':val': fieldValue,
                    ':init': 0
                }
            )
            # print 'Key=' + {
            #         TIME_HEADER: timeKey,
            #         KEYWORD_HEADER: keyword
            #     }
            # print 'UpdateExpression: ' + "set " + fieldName + " = " + fieldName + decimal.Decimal(fieldValue)

    try:
        while True:
            try:
                out = kinesis.get_records(ShardIterator=shard_it)
                for o in out["Records"]:
                    data = json.loads(o["Data"])
                    # Work with data here.

                    timeKey = getTimeKey()
                    # print data
                    if data[KEY_TYPE] == REDDIT:
                        # Find keywords from the title.
                        title = data['title']
                        keywords = extract_keywords(title)

                        # Extract score and number of comments.
                        score = data['score']
                        num_comments = data['num_comments']
                        # print keywords
                        # Put these into Dynamo
                        table =  dynamodb.Table(REDDIT_LIVE_TABLE_NAME)

                        updateFieldInTable(table, REDDIT_TABLE_NUM_COMMENTS_HEADER, num_comments, timeKey, keywords)
                        updateFieldInTable(table, REDDIT_TABLE_SCORE_HEADER, score, timeKey, keywords)
                    elif data[KEY_TYPE] == MEETUP:
                        # Find keywords from the name.
                        event_name = data['name']
                        keywords   = extract_keywords(event_name)
                        if 'description' in data:
                            keywords += extract_keywords(data['description'])

                        # Extract venue
                        # NOTE: May not be present
                        venue = "None"
                        state = "None"
                        if 'venue' in data:
                            city        = data['venue']['city']
                            country     = data['venue']['country']
                            if 'state' in data['venue']:
                                state   = data['venue']['state']
                            venue          = data['venue']['name']
                            if 'address_1' in data['venue']:
                                venue += data['venue']['address_1']
                            if 'address_2' in data['venue']:
                                venue += data['venue']['address_2']
                            if 'address_3' in data['venue']:
                                venue += data['venue']['address_3']
                        else:
                            city        = data['group']['city']
                            country     = data['group']['country']
                            if 'state' in data['group']:
                                state   = data['group']['state']

                        if 'group' in data and 'category' in data['group']['category'] and 'shortname' in data['group']['category']['shortname']:
                        # Extract category
                            event_category = data['group']['category']['shortname']
                        else:
                            event_category = 'None'

                        # Put these into Dynamo
                        table =  dynamodb.Table(MEETUPS_TABLE_NAME)

                        for keyword in keywords:
                            table.put_item(
                                Item={
                                        TIME_HEADER:     timeKey,                           # Part of key. To filter on time.
                                        KEYWORD_HEADER:  keyword,                           # Part of key.
                                        MEETUPS_LOCATION_CITY_KEY_HEADER: city,             # Part of key. To filter on geography.
                                        MEETUPS_LOCATION_STATE_KEY_HEADER: state,           # Part of key. To filter on geography.
                                        MEETUPS_LOCATION_COUNTRY_KEY_HEADER: country,       # Part of key. To filter on geography.
                                        MEETUPS_TABLE_CATEGORY_HEADER: event_category,      # Part of key. To allow searching for popular meetups according to category.
                                        MEETUPS_TABLE_NAME_HEADER:     event_name,          # Could be part of key. Will allow searching for particular events and find where they are popular.
                                        MEETUPS_TABLE_VENUE_HEADER:    venue                # Could be part of key. Will allow searching for popular events at a venue.
                                    }
                                )

                    elif data[KEY_TYPE] == TWITTER:
                        # Find keywords from the title.
                        if 'text' in data:
                            title       = data['text']
                            keywords    = extract_keywords(title)

                            # Extract number of retweets, favorites, and replies.
                            retweets    = data['retweet_count']
                            favorites   = data['favorite_count']
                            replies     = data['reply_count']

                            # Put these into Dynamo.
                            table       = dynamodb.Table(TWITTER_LIVE_TABLE_NAME)

                            updateFieldInTable(table, TWITTER_TABLE_RETWEETS_HEADER, retweets, timeKey, keywords)
                            updateFieldInTable(table, TWITTER_TABLE_FAVORITES_HEADER, favorites, timeKey, keywords)
                            updateFieldInTable(table, TWITTER_TABLE_REPLIES_HEADER, replies, timeKey, keywords)
                    else:
                        print ("Invalid data type!")

                shard_it = out["NextShardIterator"]
            except KeyError as e:
                pass
            # Try without sleep
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except:
        consumer(shard_id)

if __name__ == '__main__':
    # Spawn process for each shard.

    kinesis = boto3.client('kinesis',
                            region_name = AWS_REGION_NAME,
                            aws_access_key_id = AWS_ACCESS_KEY_ID,
                            aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

    consumer_processes = []

    shardIds = ['shardId-0000000000021', 'shardId-0000000000022', 'shardId-0000000000023']

    for shardId in shardIds:
        consumer_processes.append(Process(target=consumer, args=(shardId,)))

    for consumer_process in consumer_processes:
        consumer_process.start()

    for consumer_process in consumer_processes:
        consumer_process.join()
