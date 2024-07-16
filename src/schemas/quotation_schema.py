from datetime import date
from typing import List
from pydantic import BaseModel


class GetQuotationItem(BaseModel):
    quotation_item_id: int
    quotation_id: int
    iddetalhe: str
    cdprincipal: str
    dsdetalhe: str
    qtitem: float

class GetQuotation(BaseModel):
    quotation_id: int
    description: str
    created_at: date
    status: bool
    items: List[GetQuotationItem]
