from typing import List, TypeVar, Generic
from sqlalchemy.orm import Session
from src.model.family import Family
from src.model.base import Base as BaseModel



class BaseRepository:

    def __init__(self, session: Session, model) -> None:
        self.session: Session = session
        self.model = model
        
    def find_all(self) -> List:
        result: List  = self.session.query(self.model).all()
        self.session.close()
        return result
