from typing import List
#app
from src.model.grupoconstrufacil.quotation import Quotation
from src.repository.quotation_repository import QuotationRepository
from src.repository.quotitem_repository import QuotItemRepository
from src.schemas.purchase_suggestion_schema import CreateQuotationSchema, PurchaseSuggestionSchema
from src.schemas.quotation_schema import GetQuotation


class QuoteService:

    def find_all(self) -> List[Quotation]:
        quotation_repo = QuotationRepository()
        return quotation_repo.find_all()
    
    def find_by_quote_id(self, quotation_id) -> GetQuotation:
        quotation_repo = QuotationRepository()
        return quotation_repo.find_by_id(quotation_id)[0]
    
    def create_quotation(self, quotation: CreateQuotationSchema):
        quotation_repo = QuotationRepository()
        quotitem_repo = QuotItemRepository()
        quotation_id = quotation_repo.create(quotation.title)
        quotitem_repo.bulk_create(quotation_id, quotation.products)
        
    def delete_quotation(self, quotation_id):
        quotation_repo = QuotationRepository()
        return quotation_repo.delete(quotation_id)

    
