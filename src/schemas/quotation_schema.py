from datetime import date
from typing import List, Union
from pydantic import BaseModel


class GetQuotationItem(BaseModel):
    quotation_item_id: int
    quotation_id: int
    iddetalhe: str
    cdprincipal: str
    dsdetalhe: str
    qtitem: float

class GetQuotationSubmitItem(BaseModel):
    submission_item_id: int
    submission_id: int
    item_name: str
    qtitem: int|None
    item_brand: str|None
    item_price: float|None
    item_brand2: str|None
    item_price2: float|None


class GetQuotation(BaseModel):
    quotation_id: int
    description: str
    created_at: date
    status: bool
    items: List[GetQuotationItem]

class GetQuotationSubmit(BaseModel):
    quotation_id: int
    submission_id: int
    user_id: int
    user_name: str
    items: List[GetQuotationSubmitItem]


class Item(BaseModel):
    item_name: str
    item_brand: Union[str, None]
    item_price: Union[float, None]
    qtitem: Union[float, None]

class UserQuotation(BaseModel):
    user_id: int
    user_name: str
    submited_count: int
    cheaper_items_count: int
    total: float
    quotation_items_count: int
    items: List[Item]
    cheaper_items_list: List[str]
