from pydantic import BaseModel

class FamilyDTO(BaseModel):
    id: str
    name: str
    