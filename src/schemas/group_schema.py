from pydantic import BaseModel


class GetGroup(BaseModel):
    id: str
    name: str