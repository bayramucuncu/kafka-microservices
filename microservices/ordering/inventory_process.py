import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import OrderStatus

producer_config = {
    'bootstrap.servers': "localhost:9092,localhost:9093",
    'client.id': "orders-validation"
}
producer = KafkaProducer(producer_config)

consumer_conf = {
    'bootstrap.servers': "localhost:9092,localhost:9093",
    'group.id': "consume-submitted-orders-for-inventory",
    'auto.offset.reset': 'smallest'
}
consumer = KafkaConsumer(consumer_conf)


def msg_process(msg):
    order = json.loads(msg.value().decode("utf-8"))

    # Checking from database.
    if order["count"] > 5:
        validate_order(order)
        order["status"] = OrderStatus.Validated.value
        print("Order validated: {}".format(order))
    else:
        order["status"] = OrderStatus.OutOfStock.value
        print("Order has not been validated: {}".format(order))


def validate_order(order):
    data = json.dumps(order)
    producer.produce("validated-orders", order["order_id"], data)


consumer.start_consumer(["submitted-orders"], msg_process)
