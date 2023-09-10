import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import OrderStatus

consumer_conf = {
    'bootstrap.servers': "localhost:9092,localhost:9093",
    'group.id': "consume-accepted-accepted-for-delivery",
    'auto.offset.reset': 'smallest'
}
consumer = KafkaConsumer(consumer_conf)

producer_config = {
    'bootstrap.servers': "localhost:9092,localhost:9093",
    'client.id': "delivery_process"
}
producer = KafkaProducer(producer_config)


def start_order_delivery(order):
    # Call delivery service.
    order["status"] = OrderStatus.Shipped.value
    print("Delivery process started for {}".format(order))


def msg_process(msg):
    order = json.loads(msg.value().decode("utf-8"))

    # Checking from database.
    if order["status"] == OrderStatus.Accepted.value:
        start_order_delivery(order)


consumer.start_consumer(["accepted-orders"], msg_process)
