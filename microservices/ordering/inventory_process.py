import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer
from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import OrderStatus

consumer = KafkaConsumer("consume_submitted_orders_for_inventory")
producer = KafkaProducer("inventory_process")


def msg_process(msg):
    order = json.loads(msg.value().decode("utf-8"))

    # Checking from database.
    if order["count"] > 5:
        order["status"] = OrderStatus.Validated.value
        print("Order validated: {}".format(order))
        # Save to database.
        send_to_validate_order(order)
    else:
        order["status"] = OrderStatus.OutOfStock.value
        print("Order has not been validated: {}".format(order))
        # Save to database.


def send_to_validate_order(order):
    data = json.dumps(order)
    producer.produce("validated-orders", order["order_id"], data)


consumer.start_consumer(["submitted-orders"], msg_process)
