import json
import sys

from confluent_kafka import Consumer, KafkaError, KafkaException


class KafkaConsumer:
    consumer_configuration = {
        'bootstrap.servers': "localhost:9092,localhost:9093",
        'auto.offset.reset': 'latest'
    }

    def __init__(self, group_id):
        self.consumer_configuration["group.id"] = group_id
        self.consumer = Consumer(self.consumer_configuration)
        self.running = True

    @staticmethod
    def json_serializer(message):
        return json.dumps(message).encode('utf-8')

    def start_consumer(self, topics, callback=None):
        try:
            self.consumer.subscribe(topics)

            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    callback(msg)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def stop_consumer(self):
        self.running = False

    @staticmethod
    def print_message(message):
        print(json.dumps(message))
