import random
import string
import time

from microservices.infrastructure.kafka_producer import KafkaProducer
from microservices.models.order import Order

producer = KafkaProducer("order_process")

while True:
    o = Order(card_number=''.join(random.choices(string.digits, k=16)), count=random.randint(1, 10))
    producer.produce("submitted-orders", key=o.order_id, data=o.to_json())
    producer.poll(1)
    time.sleep(2)
