from pydantic import BaseModel


class GetPerson(BaseModel):
    id: str
    name: str