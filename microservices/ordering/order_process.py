import datetime
import json
import random
import string
import time
from typing import Any

from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import Order

producer = KafkaProducer("order_process")


def producer_acked(err: Any, msg: Any):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        order = json.loads(msg.value().decode("utf-8"))
        data = json.dumps({
            "order_id": order["order_id"],
            "report_ts": str(datetime.datetime.now()),
            "message": "Order submitted"
        })
        producer.produce("submitted-orders", key=o.order_id, data=data)
        print("Message produced: %s" % (str(msg.value().decode("utf-8"))))


while True:
    o = Order(card_number=''.join(random.choices(string.digits, k=16)), count=random.randint(1, 10))
    producer.produce("submitted-orders", key=o.order_id, data=o.to_json(), callback=producer_acked)
    producer.poll(1)
    time.sleep(2)
