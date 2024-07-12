from pydantic import BaseModel


class PurchaseSuggestionSchema(BaseModel):
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

    class Config:
        orm_mode: bool = True
