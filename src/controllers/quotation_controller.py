#std
from typing import List
#ext
from fastapi import APIRouter, Body
#app
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.schemas.quotation_schema import GetQuotation
from src.services.quote_service import QuoteService



class QuotationController:

    router = APIRouter(prefix='/quotation')

    @staticmethod
    @router.get('/', response_model=List[GetQuotation])
    def get_quotations():
        service = QuoteService()
        return service.find_all()

    @staticmethod
    @router.post('/')
    def create_quotations(products: List[PurchaseSuggestionSchema] = Body(...)):
        service = QuoteService()
        service.create_quotation(products)
        return {'message': 'Cotação criada com sucesso'}

    @classmethod
    def get_router(cls):
        return cls.router
