from pydantic import BaseModel


class GetGroup(BaseModel):
    idgrupo: str
    nmgrupo: str