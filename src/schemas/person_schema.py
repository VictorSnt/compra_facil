from pydantic import BaseModel


class GetPerson(BaseModel):
    idpessoa: str
    nmpessoa: str