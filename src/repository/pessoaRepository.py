from sqlalchemy.orm import Session
from src.model.pessoa import Pessoa


class PessoaRepository:
    
    def __init__(self, session: Session, model: Pessoa) -> None:
        self.session: Session = session
        self.model: Pessoa = model
    
    
    def find_all(self):
        return self.session.query(self.model).all()
    
    def find_all_suppliers(self):
        return self.session.query(self.model).where(self.model.sttipopessoa == 'F').all()