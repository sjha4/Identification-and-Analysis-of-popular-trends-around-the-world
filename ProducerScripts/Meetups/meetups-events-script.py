# Streaming Open Event Code

import pycurl
import json
import AWS_Creds

aws_access = AWS_Creds.AWS_ACCESS
aws_secret = AWS_Creds.AWS_SECRET

OPEN_EVENT_STREAM="http://stream.meetup.com/2/open_events"
events_data = list()

KINESIS_STREAM_NAME = "MeetupTwitterKinesisStream"

KEY_DATA = 'data'
KEY_TYPE = 'type'

DATA_TYPE = 'meetup'

MULTIPLE_POST_SEND_LIMIT = 1

def on_receive(data):
	try:
		jsonData = {}
		jsonData[KEY_TYPE] = DATA_TYPE
		jsonData[KEY_DATA] = data
		
		for i in xrange(MULTIPLE_POST_SEND_LIMIT):
			kinesis.put_record(StreamName = KINESIS_STREAM_NAME, json.dumps(jsonData), "filler")
	except KeyboardInterrupt:
    		print "Streaming interrupted by someone!"

conn = pycurl.Curl()
conn.setopt(pycurl.URL, OPEN_EVENT_STREAM)
conn.setopt(pycurl.WRITEFUNCTION, on_receive)
conn.perform()
