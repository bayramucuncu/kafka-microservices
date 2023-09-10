import json

from confluent_kafka import Producer


class KafkaProducer:

    def __init__(self, config):
        self.config = config
        self.producer = Producer(config)

    @staticmethod
    def acked(err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg.value().decode("utf-8"))))

    def produce(self, topic, key, data, callback=acked):
        self.producer.produce(topic=topic, key=key, value=data, callback=callback)

    def poll(self, timeout: float = None):
        self.producer.poll(timeout=timeout)
