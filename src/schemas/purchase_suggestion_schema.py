from typing import Dict, List
from pydantic import BaseModel


class PurchaseSuggestionSchema(BaseModel):
    iddetalhe: str
    cdprincipal: str
    dsdetalhe: str
    stock: float
    dias_suprimento: float
    sugestao: float
    dtreferencia: str
    sales: float
    security_stock: float
    avg_sales_daily: float
    avg_sales_60_days: float

    @classmethod
    def bulk_instanceate(cls, data: List[Dict]):
        response = []
        for dict_obj in data:
            if not dict_obj: continue
            if dict_obj['dias_suprimento'] > 45: continue
            response.append(cls(**dict_obj))
        return response
