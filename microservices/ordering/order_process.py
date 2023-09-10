import datetime
import json
import random
import string
import time
from typing import Any

from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import Order

order_producer = KafkaProducer("order_process")
report_producer = KafkaProducer("report_process")


def report_order(order, message):
    data = json.dumps({
        "order_id": order["order_id"],
        "report_ts": str(datetime.datetime.now()),
        "message": message
    })
    report_producer.produce("orders-reports", key=order["order_id"], data=data)


def order_acked(err: Any, msg: Any):
    if err is not None:
        print("Failed to deliver Order: %s: %s" % (str(msg), str(err)))
    else:
        report_order(json.loads(msg.value().decode("utf-8")), "Order submitted")
        print("Order produced: %s" % (str(msg.value().decode("utf-8"))))


while True:
    o = Order(card_number=''.join(random.choices(string.digits, k=16)), count=random.randint(1, 10))
    order_producer.produce("submitted-orders", key=o.order_id, data=o.to_json(), callback=order_acked)
    order_producer.poll(1)
    time.sleep(2)
