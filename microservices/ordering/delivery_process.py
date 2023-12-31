import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.ordering.report_creator import report_order
from microservices.models.order import OrderStatus

consumer = KafkaConsumer("cg_accepted_orders_1")
producer = KafkaProducer("delivery_process")


def start_order_delivery(order):
    # Call delivery service.
    order["status"] = OrderStatus.Shipped.value
    print("Delivery process started for {}".format(order))
    report_order(order, "Order delivery started")


def msg_process(msg):
    order = json.loads(msg.value().decode("utf-8"))

    # Checking from database.
    if order["status"] == OrderStatus.Accepted.value:
        start_order_delivery(order)


consumer.start_consumer(["accepted-orders"], msg_process)
