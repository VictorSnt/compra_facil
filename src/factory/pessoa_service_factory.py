from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database.db_session_maker import Session_Maker
from src.model.pessoa import Pessoa
from src.repository.pessoa_repository import PessoaRepository
from src.services.pessoa_service import PessoaService


class PessoaServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)
    ):
        repo = PessoaRepository(session, Pessoa)
        return PessoaService(repo)