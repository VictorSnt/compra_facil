from typing import List
from sqlalchemy.orm import Session
from src.model.familia import Familia


class FamiliaRepository:
    
    def __init__(self, session: Session, model: Familia) -> None:
        self.session: Session = session
        self.model: Familia = model
    
    def find_all(self) -> List[Familia]:
        result = self.session.query(self.model).all()
        self.session.close()
        return result
    
    def find_all_without_special_characters(self) -> List[Familia]:
        result = (
            self.session.query(Familia.idfamilia, Familia.dsfamilia)
            .filter(
                Familia.dsfamilia.notlike('%@%')
            )
            .order_by(Familia.dsfamilia.asc())
            .all()
        )
        self.session.close()
        return result