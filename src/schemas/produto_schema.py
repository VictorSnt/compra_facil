from pydantic import BaseModel


class GetProduto(BaseModel):
    iddetalhe: str
    dsdetalhe: str