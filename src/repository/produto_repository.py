from re import S
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from src.model.docitem import Docitem
from src.model.document import Document
from src.model.produto import Produto


class ProdutoRepository:
    
    def __init__(self, session: Session, model: Produto) -> None:
        self.session: Session = session
        self.model: Produto = model
    
    def find_all(self, active_only: bool) -> List[Produto]:
        if active_only:
            result = (
                self.session.query(self.model)
                .filter(self.model.stdetalheativo == True)
                .all()
            ) 
        else:
            result: List[Produto] = self.session.query(self.model).all()
        
        self.session.close()
        return result
