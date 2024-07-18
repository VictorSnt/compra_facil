from typing import List
#app
from src.model.grupoconstrufacil.quotation import Quotation
from src.repository.quotation_repository import QuotationRepository
from src.repository.quotitem_repository import QuotItemRepository
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema


class QuoteService:

    def find_all(self) -> List[Quotation]:
        quotation_repo = QuotationRepository()
        return quotation_repo.find_all()
    
    
    def create_quotation(self, products: List[PurchaseSuggestionSchema]):
        quotation_repo = QuotationRepository()
        quotitem_repo = QuotItemRepository()
        quotation_id = quotation_repo.create()
        quotitem_repo.bulk_create(quotation_id, products)
        
    def delete_quotation(self, quotation_id):
        quotation_repo = QuotationRepository()
        return quotation_repo.delete(quotation_id)

    
