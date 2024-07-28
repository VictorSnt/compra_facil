from typing import List
#app
from src.repository.order_item_repository import OrderItemRepository
from src.repository.quotitem_repository import QuotItemRepository
from src.schemas.order_schema import CreateOrderItems, GetOrderItem


class OrderItemService:

    def create_order_item(self, items: List[CreateOrderItems]):
        quotitem_repo = OrderItemRepository()
        quotitem_repo.bulk_create(items)

    def find_all(self) -> List[GetOrderItem]:
        quotation_repo = OrderItemRepository()
        return quotation_repo.find_all()
