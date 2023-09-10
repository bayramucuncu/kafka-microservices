import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import OrderStatus

consumer = KafkaConsumer("consume_validated_orders_for_payment")
producer = KafkaProducer("payment_process")


def accept_order(order):
    order["status"] = OrderStatus.Accepted.value
    print("Order paid and accepted: {}".format(order))
    # save to database
    data = json.dumps(order)
    producer.produce("accepted-orders", order["order_id"], data)


def cancel_order(order):
    order["status"] = OrderStatus.Cancelled.value
    print("Order payment failed and cancelled: {}".format(order))
    # save to database


def pay_order(order) -> bool:
    if order["card_number"].startswith(tuple(["0", "2", "4", "6", "8", "7", "5"])):
        return True
    else:
        return False


def msg_process(msg):
    order = json.loads(msg.value().decode("utf-8"))

    # Checking from database.
    if order["status"] == OrderStatus.Validated.value:
        is_paid = pay_order(order)
        order["status"] = OrderStatus.Paid.value
        if is_paid:
            accept_order(order)
        else:
            cancel_order(order)


consumer.start_consumer(["validated-orders"], msg_process)
