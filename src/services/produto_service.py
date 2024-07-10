from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.produto_repository import ProdutoRepository
from src.schemas.produto_schema import GetProduto

router = APIRouter()


class ProdutoService:
    
    def __init__(self, repository: ProdutoRepository) -> None:
        self.repo = repository
    
    def find_all(self, only_active: bool):
        
        response = self.repo.find_all(only_active)
        
        if not response:
            raise NotFoundException
        print('serc')
        return [
            GetProduto(
                iddetalhe=produto.iddetalhe, 
                dsdetalhe=produto.dsdetalhe
            ) for produto in response
        ]

    
