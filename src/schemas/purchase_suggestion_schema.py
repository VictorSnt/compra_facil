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

    def __init__(self, **data):
        super().__init__(**data)

        self.stock = round(self.stock, 2)
        self.dias_suprimento = round(self.dias_suprimento, 2)
        self.sugestao = round(self.sugestao, 2)
        self.sales = round(self.sales, 2)
        self.security_stock = round(self.security_stock, 2)
        self.avg_sales_daily = round(self.avg_sales_daily, 2)
        self.avg_sales_60_days = round(self.avg_sales_60_days, 2)

    @classmethod
    def bulk_instanceate(cls, data: List[Dict]):
        response = []
        for dict_obj in data:
            if not dict_obj: continue
            if dict_obj['dias_suprimento'] > 45: continue
            response.append(cls(**dict_obj))
        return response
