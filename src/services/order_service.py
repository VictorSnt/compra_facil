from typing import List
#app
from src.repository.orders_repository import OrdersRepository
from src.schemas.order_schema import CreateOrder, GetOrder


class OrderService:

    def find_all(self) -> List[GetOrder]:
        quotation_repo = OrdersRepository()
        return quotation_repo.find_all()

    def find_by_order_id(self, order_id) -> GetOrder:
        quotation_repo = OrdersRepository()
        return quotation_repo.find_by_id(order_id)[0]

    def find_by_user_id(self, user_id) -> GetOrder:
        quotation_repo = OrdersRepository()
        return quotation_repo.find_by_user(user_id)[0]

    def create_order(self, order: CreateOrder):
        quotation_repo = OrdersRepository()
        order_id = quotation_repo.create(order)
        return order_id

    def finish_order(self, order_id):
        quotation_repo = OrdersRepository()
        return quotation_repo.finish_order(order_id)
