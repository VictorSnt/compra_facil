from pydantic import BaseModel


class GetProduct(BaseModel):
    iddetalhe: str
    dsdetalhe: str
    
class GetProductWithStock(BaseModel):
    iddetalhe: str
    dsdetalhe: str
    cdprincipal: str
    stock: float