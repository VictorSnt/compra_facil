from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database.db_session_maker import Session_Maker
from src.model.person import Person
from src.repository.person_repository import PersonRepository
from src.services.person_service import PersonService


class PersonServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = PersonRepository(session, Person)
        return PersonService(repo)