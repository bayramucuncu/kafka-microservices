import datetime
import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import OrderStatus

consumer = KafkaConsumer("cg-accepted-orders_1")
order_producer = KafkaProducer("delivery_process")
report_producer = KafkaProducer("report_process")


def report_order(order, message):
    data = json.dumps({
        "order_id": order["order_id"],
        "report_ts": str(datetime.datetime.now()),
        "message": message
    })
    report_producer.produce("orders-reports", key=order["order_id"], data=data)


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
