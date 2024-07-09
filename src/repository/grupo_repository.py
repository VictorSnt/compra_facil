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
    
    def find_all_without_special_characters(self) -> List[Grupo]:
        result = (
            self.session.query(Grupo.idgrupo, Grupo.nmgrupo)
            .filter(
                Grupo.nmgrupo.notlike('%@%'),
                Grupo.nmgrupo.notlike('%*%')
            )
            .order_by(Grupo.nmgrupo.asc())
            .all()
        )
        self.session.close()
        return result