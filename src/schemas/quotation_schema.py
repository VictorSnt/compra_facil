from pydantic import BaseModel


class GetQuotation(BaseModel):
    quotation_id: int
    status: bool


class GetQuotationItem(BaseModel):
    quotation_item_id: int
    quotation_id: int
    iddetalhe: str
    cdprincipal: str
    dsdetalhe: str
    qtitem: float
