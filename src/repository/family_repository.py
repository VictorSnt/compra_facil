from typing import List
from sqlalchemy.orm import Session
from src.model.family import Family
from src.repository.base_repository import BaseRepository


class FamilyRepository(BaseRepository):

    def __init__(self, session: Session, model: Family) -> None:
        super().__init__(session, model)
        
    def find_all_without_special_characters(self, ids) -> List[Family]:
        if ids:
            result: List[Family] = (
                self.session.query(self.model)
                .filter(
                    self.model.dsfamilia.notlike('%@%'), 
                    self.model.idfamilia.in_(ids)
                ).order_by(self.model.dsfamilia.asc())
                .all()
            )
        else:
            result: List[Family] = (
                self.session.query(self.model)
                .filter(
                    self.model.dsfamilia.notlike('%@%')
                ).order_by(self.model.dsfamilia.asc())
                .all()
            )

        self.session.close()
        return result

    def find_by_id(self, id: str):
        result: List[Family] = (
            self.session.query(self.model)
            .where(self.model.idfamilia == id )
            .all()
        )
        self.session.close()
        return result
