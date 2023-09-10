import json
import uuid
from typing import Any

from confluent_kafka import Producer


class KafkaProducer:

    @staticmethod
    def json_serializer(message):
        return json.dumps(message).encode('utf-8')

    producer_config = {
        'bootstrap.servers': "localhost:9092,localhost:9093",
        'client.id': str(uuid.uuid4())
    }

    def __init__(self, client_id=None):
        self.producer_config["client.id"] = client_id
        self.producer = Producer(self.producer_config)

    @staticmethod
    def acked(err: Any, msg: Any):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg.value().decode("utf-8"))))

    def produce(self, topic, key, data, callback=None):
        self.producer.produce(topic=topic, key=key, value=data, callback=callback)

    def poll(self, timeout: float = None):
        self.producer.poll(timeout=timeout)
