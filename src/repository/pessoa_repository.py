from typing import List
from sqlalchemy.orm import Session
from src.model.pessoa import Pessoa


class PessoaRepository:
    
    def __init__(self, session: Session, model: Pessoa) -> None:
        self.session: Session = session
        self.model: Pessoa = model
    
    
    def find_all(self) -> List[Pessoa]:
        result = self.session.query(self.model).all()
        self.session.close()
        return result
    
    def find_all_suppliers(self) -> List[Pessoa]:
        result =  (
            self.session.query(self.model)
            .where(self.model.sttipopessoa == 'F')
            .all()
        )
        self.session.close()
        return result 
    