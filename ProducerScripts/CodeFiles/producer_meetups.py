import pycurl, sys
from AWS_CREDS import *

OPEN_EVENT_STREAM="http://stream.meetup.com/2/open_events"
events_data = list()

MULTIPLE_POST_SEND_LIMIT = 100
if len(sys.argv) == 2:
    MULTIPLE_POST_SEND_LIMIT = int(sys.argv[1])
KINESIS_PUT_BATCH_SIZE = MULTIPLE_POST_SEND_LIMIT / 10

KINESIS_PUT_BATCH_SIZE = 1 if KINESIS_PUT_BATCH_SIZE == 0 else KINESIS_PUT_BATCH_SIZE
KINESIS_PUT_BATCH_SIZE = 500 if KINESIS_PUT_BATCH_SIZE > 500 else KINESIS_PUT_BATCH_SIZE

leftOverData = ""

def on_receive(data):
    global leftOverData
    try:
        lines = (leftOverData + data).split("\n")
        for l in lines[:-1]:
            putDataToKinesisStream(json.loads(l), TYPE_MEETUPS, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)
        leftOverData = lines[-1]
    except KeyboardInterrupt:
    		print "Streaming interrupted by someone!"
    except Exception as e:
        print e

conn = pycurl.Curl()
conn.setopt(pycurl.URL, OPEN_EVENT_STREAM)
conn.setopt(pycurl.WRITEFUNCTION, on_receive)
conn.perform()
