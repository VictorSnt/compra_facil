from typing import List
#app
from src.repository.orders_repository import OrdersRepository
from src.schemas.order_schema import CreateOrder, GetOrder, UpdateOrderItem


class OrderService:

    def find_all(self) -> List[GetOrder]:
        orders_repo = OrdersRepository()
        return orders_repo.find_all()

    def update_order_item(self, order_item_id: int, updated_item: UpdateOrderItem):
        orders_repo = OrdersRepository()
        return orders_repo.update_order_item(order_item_id, updated_item)

    def delete_order_item(self, order_item_id: int):
        orders_repo = OrdersRepository()
        return orders_repo.delete_order_item(order_item_id)

    def find_by_order_id(self, order_id) -> GetOrder:
        orders_repo = OrdersRepository()
        return orders_repo.find_by_id(order_id)[0]

    def find_by_user_id(self, user_id) -> int:
        orders_repo = OrdersRepository()
        return orders_repo.find_by_user(user_id)

    def create_order(self, order: CreateOrder):
        orders_repo = OrdersRepository()
        order_id = orders_repo.create(order)
        return order_id

    def finish_order(self, order_id):
        orders_repo = OrdersRepository()
        return orders_repo.finish_order(order_id)
