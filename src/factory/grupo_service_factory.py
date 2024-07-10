from fastapi.params import Depends
from sqlalchemy.orm import Session


from src.database.db_session_maker import Session_Maker
from src.model.grupo import Grupo
from src.repository.grupo_repository import GrupoRepository
from src.services.grupo_services import GrupoService


class GrupoServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = GrupoRepository(session, Grupo)
        return GrupoService(repo)