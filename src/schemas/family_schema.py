from pydantic import BaseModel


class GetFamily(BaseModel):
    id: str
    name: str
    