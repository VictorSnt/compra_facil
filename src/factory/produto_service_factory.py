from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database.db_session_maker import Session_Maker
from src.model.produto import Produto
from src.repository.produto_repository import ProdutoRepository
from src.services.produto_service import ProdutoService


class ProdutoServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = ProdutoRepository(session, Produto)
        return ProdutoService(repo)
