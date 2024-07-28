#std
from typing import List
#ext
from fastapi import APIRouter, Body
#app
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.services.quote_item_service import QuoteItemService
from src.schemas.quotation_schema import GetQuotationItem


class QuotationItemController:

    router = APIRouter(prefix='/quotation_item')

    @staticmethod
    @router.get('/', response_model=List[GetQuotationItem])
    def get_quotation_items():
        service = QuoteItemService()
        return service.find_all()

    @staticmethod
    @router.post('/')
    def create_quotation_items(
        products: List[PurchaseSuggestionSchema] = Body(...)
    ):
        service = QuoteItemService()
        service.create_quotation('title', products)
        return {'message': 'Criado com sucesso'}

    @classmethod
    def get_router(cls):
        return cls.router
