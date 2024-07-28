from typing import List
from pydantic import BaseModel

class CreateOrder(BaseModel):
    user_id: int

class CreateOrderItems(BaseModel):
    order_id: int
    quotation_item_id: int
    iddetalhe: str
    dsdetalhe: str
    qtcompra: float
    vlcompra: float

class GetOrderItens(CreateOrderItems):
    order_item_id: int


class GetOrder(CreateOrder):
    order_id: int
    user_name: str
    items: List[GetOrderItens]
    