#ext
from fastapi import Depends
from sqlalchemy.orm import Session
#app
from src.database.db_session_maker import SessionMaker
from src.model.family import Family
from src.repository.family_repository import FamilyRepository
from src.services.family_service import FamilyService


class FamilyServiceFactory:
    
    @classmethod
    def build_default_service(
        cls, session: Session = Depends(SessionMaker.create_session)):
        
        repo = FamilyRepository(session, Family)
        return FamilyService(repo)