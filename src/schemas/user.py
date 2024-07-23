from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    cnpj: str
    email: str
