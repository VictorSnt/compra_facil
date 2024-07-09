from pydantic import BaseModel


class GetGrupo(BaseModel):
    idgrupo: str
    nmgrupo: str