#std
from typing import List
#ext
from fastapi import APIRouter, Body, HTTPException, Path
#app
from src.schemas.order_schema import CreateOrder, GetOrder, GetOrderItens
from src.services.order_service import OrderService



class OrderControlle:

    router = APIRouter(prefix='/order')

    @staticmethod
    @router.get('/{order_id}', response_model=List[GetOrder])
    def get_orders_by_id(order_id: str =  Path()):
        service = OrderService()
        orders = service.find_by_order_id(order_id)
        return orders

    @staticmethod
    @router.get('/{user_id}', response_model=List[GetOrderItens])
    def get_orders_by_user_id(user_id: str =  Path()):
        service = OrderService()
        orders = service.find_by_user_id(user_id)
        return orders

    @staticmethod
    @router.post('/{order_id}')
    def finish_order(order_id: str = Path()):
        service = OrderService()
        service.finish_order(order_id)
        return {'message': 'pedido finalizado'}

    @staticmethod
    @router.post('/')
    def create_orders(quotation: CreateOrder = Body(...)):
        service = OrderService()
        return service.create_order(quotation)

    @staticmethod
    @router.get('/', response_model=List[GetOrder])
    def get_orders():
        service = OrderService()
        return service.find_all()

    @staticmethod
    @router.post('/user/{user_id}', response_model=int)
    def get_or_create(user_id: str = Path()):
        service = OrderService()
        try:
            order_id = service.find_by_user_id(user_id)
            return order_id
        except HTTPException as e:
            print(e)
            return service.create_order(CreateOrder(user_id=user_id))

    @classmethod
    def get_router(cls):
        return cls.router
