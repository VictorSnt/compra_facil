from typing import List
#app
from src.model.grupoconstrufacil.quotation import Quotation
from src.repository.quotation_repository import QuotationRepository
from src.repository.quotitem_repository import QuotItemRepository
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema


class QuoteItemService:

    def create_quotation(self, title, products: List[PurchaseSuggestionSchema]):

        quotation_repo = QuotationRepository()
        quotitem_repo = QuotItemRepository()
        quotation_id = quotation_repo.create(title)
        quotitem_repo.bulk_create(quotation_id, products)

    def find_all(self) -> List[Quotation]:
        quotation_repo = QuotItemRepository()
        return quotation_repo.find_all()
