from pydantic import BaseModel


class GetPessoa(BaseModel):
    idpessoa: str
    nmpessoa: str