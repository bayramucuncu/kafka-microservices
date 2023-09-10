import datetime
import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import OrderStatus

order_consumer = KafkaConsumer("cg_validated_orders_1")
order_producer = KafkaProducer("payment_process")
report_producer = KafkaProducer("report_process")


def report_order(order, message):
    data = json.dumps({
        "order_id": order["order_id"],
        "report_ts": str(datetime.datetime.now()),
        "message": message
    })
    report_producer.produce("orders-reports", key=order["order_id"], data=data)


def accept_order(order):
    order["status"] = OrderStatus.Accepted.value
    print("Order paid and accepted: {}".format(order))
    # save to database
    data = json.dumps(order)
    order_producer.produce("accepted-orders", order["order_id"], data)
    report_order(order, "Order accepted")


def cancel_order(order):
    order["status"] = OrderStatus.Cancelled.value
    print("Order payment failed and cancelled: {}".format(order))
    # save to database
    report_order(order, "Order payment failed, so order did not accepted")


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


order_consumer.start_consumer(["validated-orders"], msg_process)
