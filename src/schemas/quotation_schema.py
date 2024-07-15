from pydantic import BaseModel


class GetQuotation(BaseModel):
    quotation_id: int
    status: bool
