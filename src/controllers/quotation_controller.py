#std
from typing import List
#ext
from fastapi import APIRouter, Body, Path
#app
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.schemas.quotation_schema import GetQuotation, GetQuotationItem
from src.services.quote_service import QuoteService



class QuotationController:

    router = APIRouter(prefix='/quotation')

    @staticmethod
    @router.get('/', response_model=List[GetQuotation])
    def get_quotations():
        service = QuoteService()
        return service.find_all()
    
    @staticmethod
    @router.get('/{quotation_id}/items', response_model=List[GetQuotationItem])
    def get_quotations(quotation_id: str =  Path()):
        service = QuoteService()
        quotes = service.find_by_quote_id(quotation_id)
        return quotes.items
    
    @staticmethod
    @router.post('/')
    def create_quotations(products: List[PurchaseSuggestionSchema] = Body(...)):
        service = QuoteService()
        service.create_quotation(products)
        return {'message': 'Cotação criada com sucesso'}

    @staticmethod
    @router.delete('/{quotation_id}')
    def finish_quotation(quotation_id: str =  Path()):
        service = QuoteService()
        service.delete_quotation(quotation_id)
        return {'message': 'Cotação encerrada'}
    
    
    @classmethod
    def get_router(cls):
        return cls.router
