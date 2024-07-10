from pydantic import BaseModel


class GetProduct(BaseModel):
    iddetalhe: str
    dsdetalhe: str