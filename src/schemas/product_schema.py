from pydantic import BaseModel


class GetProduct(BaseModel):
    iddetalhe: str
    dsdetalhe: str
    bla: None|float = None
    
class GetProductWithStock(BaseModel):
    iddetalhe: str
    dsdetalhe: str
    cdprincipal: str
    stock: float