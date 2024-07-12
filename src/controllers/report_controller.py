#std
from typing import List
#ext
from fastapi import APIRouter, Query, Depends
#app
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.factory.report_service_factory import ReportServiceFactory
from src.services.report_service import ReportService


class ReportController:

    router = APIRouter(prefix="/report")

    @staticmethod
    @router.get(
        '/shopping_suggestion', 
        response_model=List[PurchaseSuggestionSchema])
    def shopping_suggestion(
        service: ReportService = Depends(
            ReportServiceFactory.build_default_service
        ),
        product_ids: List[str] = Query()
    ):
        response = service.shopping_suggestion(product_ids)
        return response

    
    @staticmethod
    @router.get(
        '/cache_suggestions', 
        response_model=List[PurchaseSuggestionSchema])
    def cache_suggestions(
        service: ReportService = Depends(
            ReportServiceFactory.build_default_service
        ),
        repositions_days: int = Query(60)
    ):
        return service.cache_suggestions(repositions_days)
        
    @staticmethod
    @router.get(
        '/generate_quote', 
        response_model=List[PurchaseSuggestionSchema])
    def generate_quote(
        service: ReportService = Depends(
            ReportServiceFactory.build_default_service)):
        
        return service.generate_quote()
    
    
    @classmethod
    def get_router(cls):
        return cls.router
