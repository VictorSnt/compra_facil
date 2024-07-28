#std
from typing import List
#ext
from fastapi import APIRouter, Body
#app
from src.services.order_item_service import OrderItemService
from src.schemas.order_schema import GetOrderItem, CreateOrderItems


class OrderItemController:

    router = APIRouter(prefix='/order_item')

    @staticmethod
    @router.get('/', response_model=List[GetOrderItem])
    def get_order_items():
        service = OrderItemService()
        return service.find_all()

    @staticmethod
    @router.post('/')
    def create_order_items(
        items: List[CreateOrderItems] = Body(...)
    ):
        service = OrderItemService()
        service.create_order_item(items)
        return {'message': 'Criado com sucesso'}

    @classmethod
    def get_router(cls):
        return cls.router
