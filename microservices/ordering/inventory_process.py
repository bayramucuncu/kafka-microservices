import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.ordering.report_creator import report_order
from microservices.models.order import OrderStatus

order_consumer = KafkaConsumer("cg_submitted_orders_1")
inventory_producer = KafkaProducer("inventory_process")
report_producer = KafkaProducer("report_process")


def msg_process(msg):
    order = json.loads(msg.value().decode("utf-8"))
    # Checking from database.
    if order["count"] > 5:
        order["status"] = OrderStatus.Validated.value
        print("Order validated: {}".format(order))
        # Save to database.
        send_to_validate_order(order)
        report_order(order, "Order validated")
    else:
        order["status"] = OrderStatus.OutOfStock.value
        print("Order has not been validated: {}".format(order))
        # Save to database.
        report_order(order, "Order has not been validated, because product is of out of stock")


def send_to_validate_order(order):
    data = json.dumps(order)
    inventory_producer.produce("validated-orders", order["order_id"], data)


order_consumer.start_consumer(["submitted-orders"], msg_process)
