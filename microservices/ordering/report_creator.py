import datetime
import json

from microservices.infrastructure.kafka_producer import KafkaProducer

report_producer = KafkaProducer("report_process")


def report_order(order, message):
    data = json.dumps({
        "order_id": order["order_id"],
        "report_ts": str(datetime.datetime.now()),
        "message": message
    })
    report_producer.produce("orders-reports", key=order["order_id"], data=data)