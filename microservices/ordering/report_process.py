import json

from microservices.infrastructure.kafka_consumer import KafkaConsumer

consumer = KafkaConsumer("cg_orders_reports_1")


def msg_process(msg):
    report = json.loads(msg.value().decode("utf-8"))
    print(report)


consumer.start_consumer(["orders-reports"], msg_process)
