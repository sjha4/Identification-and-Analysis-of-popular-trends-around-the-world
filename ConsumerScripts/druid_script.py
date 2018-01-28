from kafka import KafkaConsumer

# Consumer subscribes to the topic in this list.
topics_list = []

kafka_wait_time_for_stream_read = 2000 # In Milli seconds

settings = {
    'bootstrap.servers': 'localhost:9092', # Set this!
    'group.id': 'mygroup', # ?
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}

kafka_consumer = KafkaConsumer(settings)

kafka_consumer.subscribe(topics_list)

try:
    while True:
        msg = kafka_consumer.poll(timeout_ms=kafka_wait_time_for_stream_read)
        if msg is None:
            continue
        elif not msg.error():
            print('Received message: {0}'.format(msg.value()))
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'
                  .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))
            
except KeyboardInterrupt:
    pass

finally:
    kafka_consumer.close()