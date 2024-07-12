#std
from typing import List
#ext
from fastapi import APIRouter, Query, Depends
#app
from src.schemas.purchase_sugestion_schema import PurchaseSuggestionSchema
from src.factory.report_service_factory import ReportServiceFactory
from src.services.report_service import ReportService


class ReportController:

    router = APIRouter(prefix="/report")

    @staticmethod
    @router.get(
        '/shopping_sugestion', 
        response_model=List[PurchaseSuggestionSchema])
    def shopping_sugestion(
        service: ReportService = Depends(
            ReportServiceFactory.build_default_service
        ),
        product_ids: List[str] = Query()
    ):
        response = service.shopping_suggestion(product_ids)
        return response

    @classmethod
    def get_router(cls):
        return cls.router
