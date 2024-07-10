from fastapi import APIRouter

from src.repository.pessoa_repository import PessoaRepository
from src.exceptions.err import NotFoundException
from src.schemas.pessoa_schema import GetPessoa


router = APIRouter()


class PessoaService:
    
    def __init__(self, repository: PessoaRepository) -> None:
        self.repo = repository
    
    def find_all(self):
        
        response = self.repo.find_all()
        
        if not response:
            raise NotFoundException
        
        return [
            GetPessoa(idpessoa=pessoa.idpessoa, nmpessoa=pessoa.nmpessoa) 
            for pessoa in response
        ]

    def find_all_suppliers(self):
        
        response = self.repo.find_all_suppliers()
        
        if not response:
            raise NotFoundException
        
        return [
            GetPessoa(idpessoa=pessoa.idpessoa, nmpessoa=pessoa.nmpessoa) 
            for pessoa in response
        ]
