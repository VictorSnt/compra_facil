#std
from typing import List
#ext
from fastapi import APIRouter, Path
#app
from src.schemas.quotation_schema import GetQuotationSubmit, UserQuotation
from src.services.quote_submit_service import QuoteSubmitService



class QuotationSubmitController:

    router = APIRouter(prefix='/quotation_submit')

    @staticmethod
    @router.get('/{quotation_id}', response_model=List[GetQuotationSubmit])
    def get_quotations_submitons(quotation_id: int = Path()):
        service = QuoteSubmitService()
        return service.find_by_id(quotation_id)
        
    @staticmethod
    @router.get('/processed/{quotation_id}', response_model=List[UserQuotation])
    def process_quotations(quotation_id: int = Path()):
        service = QuoteSubmitService()
        quotes = service.find_by_id(quotation_id)
        return service.process_quotations(quotes)
        
    @classmethod
    def get_router(cls):
        return cls.router
