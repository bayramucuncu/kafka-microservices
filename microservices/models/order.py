import datetime
import json
import uuid
from enum import Enum


class OrderStatus(str, Enum):
    Accepted = "accepted"
    Submitted = "submitted"
    Cancelled = "cancelled"
    Validated = "validated"
    Paid = "paid"
    Shipped = "shipped"
    OutOfStock = "out_of_stock"


class Order:
    status: OrderStatus
    order_id: uuid
    created_ts: datetime
    status: OrderStatus
    card_number: str

    def __init__(self, card_number: str, order_id: str = None, create_ts: str = None, count: int = 0,
                 status: OrderStatus = OrderStatus.Submitted):
        self.order_id = order_id or str(uuid.uuid4())
        self.created_ts = create_ts or str(datetime.datetime.now())
        self.count = count
        self.status: OrderStatus = status
        self.card_number = card_number

    def set_status(self, status: OrderStatus):
        self.status = status

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_json(self):
        return self.__str__()
