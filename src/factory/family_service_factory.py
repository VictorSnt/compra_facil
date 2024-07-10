from fastapi.params import Depends
from sqlalchemy.orm import Session


from src.database.db_session_maker import Session_Maker
from src.model.family import Family
from src.repository.family_repository import FamilyRepository
from src.services.family_service import FamilyService


class FamilyServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = FamilyRepository(session, Family)
        return FamilyService(repo)