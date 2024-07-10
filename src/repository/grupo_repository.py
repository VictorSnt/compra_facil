from typing import List
from sqlalchemy.orm import Session
from src.model.grupo import Grupo


class GrupoRepository:
    
    def __init__(self, session: Session, model: Grupo) -> None:
        self.session: Session = session
        self.model: Grupo = model
    
    def find_all(self) -> List[Grupo]:
        result = self.session.query(self.model).all()
        self.session.close()
        return result
    
    def find_all_without_special_characters(self, ids) -> List[Grupo]:
        if ids:
            result = (
                self.session.query(self.model)
                .filter(
                    self.model.nmgrupo.notlike('%@%'),
                    self.model.nmgrupo.notlike('%*%'),
                    self.model.idgrupo.in_(ids)
                    
                )
                .order_by(self.model.nmgrupo.asc())
                .all()
            )
            self.session.close()
            
        else:
            result = (
                self.session.query(self.model)
                .filter(
                    self.model.nmgrupo.notlike('%@%'),
                    self.model.nmgrupo.notlike('%*%')
                )
                .order_by(self.model.nmgrupo.asc())
                .all()
            )
            
        return result
