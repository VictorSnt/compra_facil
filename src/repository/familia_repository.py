from typing import List
from sqlalchemy.orm import Session
from src.model.familia import Familia


class FamiliaRepository:
    
    def __init__(self, session: Session, model: Familia) -> None:
        self.session: Session = session
        self.model: Familia = model
    
    def find_all(self) -> List[Familia]:
        result: List[Familia] = self.session.query(self.model).all()
        self.session.close()
        return result
    
    def find_all_without_special_characters(self, ids) -> List[Familia]:
        if ids:
            result: List[Familia] = (
                self.session.query(self.model)
                .filter(
                    self.model.dsfamilia.notlike('%@%'), 
                    self.model.idfamilia.in_(ids)
                ).order_by(self.model.dsfamilia.asc())
                .all()
            )
        else:
            result: List[Familia] = (
                self.session.query(self.model)
                .filter(
                    self.model.dsfamilia.notlike('%@%')
                ).order_by(self.model.dsfamilia.asc())
                .all()
            )
        
        self.session.close()
        return result
    
    def find_by_id(self, id: str):
        result: List[Familia] = (
            self.session.query(self.model)
            .where(self.model.idfamilia == id )
            .all()
        )
        self.session.close()
        return result