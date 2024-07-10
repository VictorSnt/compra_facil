from typing import List
from sqlalchemy.orm import Session
from src.model.person import Person


class PersonRepository:
    
    def __init__(self, session: Session, model: Person) -> None:
        self.session: Session = session
        self.model: Person = model
    
    
    def find_all(self) -> List[Person]:
        result = self.session.query(self.model).all()
        self.session.close()
        return result
    
    def find_all_suppliers(self) -> List[Person]:
        result =  (
            self.session.query(self.model)
            .where(self.model.sttipopessoa == 'F')
            .all()
        )
        self.session.close()
        return result 
    