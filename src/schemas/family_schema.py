from pydantic import BaseModel


class GetFamily(BaseModel):
    idfamilia: str
    dsfamilia: str
    