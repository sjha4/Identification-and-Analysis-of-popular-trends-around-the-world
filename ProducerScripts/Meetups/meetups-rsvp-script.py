# Streaming RSVP Code
import pycurl
import json


RSVP_STREAM="http://stream.meetup.com/2/rsvps"

streams_data = list()

def on_receive(data):
    try:
        jsonData = json.dumps(data)
  		#recordData = {'Data':jsonData, 'PartitionKey':"filler"}
		for i in xrange(2000):
			kinesis.put_record(StreamName="MeetupTwitterKinesisStream", jsonData, "filler")
    except KeyboardInterrupt:
        print "Streaming Services halted by the user."

conn = pycurl.Curl()
conn.setopt(pycurl.URL, RSVP_STREAM)
conn.setopt(pycurl.WRITEFUNCTION, on_receive)
conn.perform()
