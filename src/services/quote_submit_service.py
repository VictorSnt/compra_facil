from typing import List, Dict
#app
from src.repository.quote_submit_repository import QuotSubimitRepository
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.schemas.quotation_schema import GetQuotationSubmit, Item, UserQuotation
from src.usecase.quotation_processor import QuotationProcessor

class QuoteSubmitService:

    def find_by_id(self, quotation_id: int) -> List[PurchaseSuggestionSchema]:
        quotation_repo = QuotSubimitRepository()
        return quotation_repo.find_by_id(quotation_id)

    def process_quotations(self, quotations: List[GetQuotationSubmit]) -> List[UserQuotation]:
        quote_processor = QuotationProcessor()
        res = quote_processor.process_quotations(quotations)
        return res
