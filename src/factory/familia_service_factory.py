from fastapi.params import Depends
from sqlalchemy.orm import Session


from src.database.db_session_maker import Session_Maker
from src.model.familia import Familia
from src.repository.familia_repository import FamiliaRepository
from src.services.familia_service import FamiliaService


class FamiliaServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = FamiliaRepository(session, Familia)
        return FamiliaService(repo)