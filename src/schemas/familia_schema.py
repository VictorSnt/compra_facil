from pydantic import BaseModel


class GetFamilia(BaseModel):
    idfamilia: str
    dsfamilia: str
    