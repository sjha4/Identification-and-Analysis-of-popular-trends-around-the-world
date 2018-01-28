import boto3
import json

# AWS credentials
AWS_SECRET_ACCESS_KEY   = 'BJCYwL5zAEIt3hPGZnfkt3RBU1SAYgjQRlKqGzfX'
AWS_ACCESS_KEY_ID       = 'AKIAIUXWPXCNXXZQKZQA'
AWS_REGION_NAME         = 'us-east-1'
AWS_STREAM_NAME         = 'DIC_MRT'

TOTAL_SHARDS = 0

kinesis = boto3.client('kinesis', region_name=AWS_REGION_NAME, \
    aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

explicit_hash_keys = []

KEY_DATA = 'Data'
KEY_TYPE = 'type'

TYPE_REDDIT     = 'reddit'
TYPE_TWITTER    = 'twitter'
TYPE_MEETUPS    = 'meetup'

stream_description = kinesis.describe_stream(StreamName=AWS_STREAM_NAME)

for shard in stream_description['StreamDescription']['Shards']:
    TOTAL_SHARDS += 1
    explicit_hash_keys.append(shard['HashKeyRange']['StartingHashKey'])

def putDataToKinesisStream(data, data_type, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE):
    if data_type == TYPE_REDDIT:
        data = vars(data)
        data.pop('subreddit', None)
        data.pop('author', None)
        data.pop('_reddit', None)

    data[KEY_TYPE] = data_type
    dataSet = []

    shard = 0
    i = 0

    while i <= MULTIPLE_POST_SEND_LIMIT:
        if i != 0 and i % KINESIS_PUT_BATCH_SIZE == 0:
            kinesis.put_records(StreamName = AWS_STREAM_NAME, Records = dataSet)
            dataSet = []
        dataSet.append({KEY_DATA: json.dumps(data), 'ExplicitHashKey': explicit_hash_keys[shard], 'PartitionKey': str(hash("partition-" + str(shard)))})
        i += 1
        shard += 1
        if shard == TOTAL_SHARDS: shard = 1

    if dataSet:
        kinesis.put_records(StreamName = AWS_STREAM_NAME, Records = dataSet)
