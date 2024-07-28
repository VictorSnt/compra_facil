#std
from typing import List
#ext
from fastapi import APIRouter, Body, HTTPException, Path
#app
from src.schemas.order_schema import CreateOrder, GetOrder, GetOrderItem
from src.services.order_service import OrderService, UpdateOrderItem



class OrderControlle:

    router = APIRouter(prefix='/order')

    @staticmethod
    @router.get('/{order_id}', response_model=List[GetOrder])
    def get_orders_by_id(order_id: str =  Path()):
        service = OrderService()
        orders = service.find_by_order_id(order_id)
        return orders

    @staticmethod
    @router.get('/{order_id}/items', response_model=List[GetOrderItem])
    def get_items_by_order_id(order_id: str =  Path()):
        service = OrderService()
        orders = service.find_by_order_id(order_id)
        if not orders.items:
            raise HTTPException(
                404, 'Nenhum item nesse pedido'
            )
        return orders.items

    @staticmethod
    @router.put('/item/{order_item_id}', response_model=GetOrderItem)
    def update_order_item(
        order_item_id: str = Path(),
        updated_item: UpdateOrderItem = Body()
    ):
        service = OrderService()
        return service.update_order_item(order_item_id, updated_item)

    @staticmethod
    @router.delete('/item/{order_item_id}', response_model=GetOrderItem)
    def delete_order_item(order_item_id: str = Path(),):
        service = OrderService()
        return service.delete_order_item(order_item_id)

    @staticmethod
    @router.get('/{user_id}', response_model=List[GetOrderItem])
    def get_orders_by_user_id(user_id: str =  Path()):
        service = OrderService()
        orders = service.find_by_user_id(user_id)
        return orders

    @staticmethod
    @router.delete('/{order_id}')
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
