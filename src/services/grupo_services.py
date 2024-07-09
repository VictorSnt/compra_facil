from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.grupo_repository import GrupoRepository
from src.schemas.grupo_schema import GetGrupo

router = APIRouter()


class GrupoService:
    
    def __init__(self, repository: GrupoRepository) -> None:
        self.repo = repository
    
    def find_all(self):
        
        response = self.repo.find_all()
        
        if not response:
            raise NotFoundException
        
        return [
            GetGrupo(idgrupo=grupo.idgrupo, nmgrupo=grupo.nmgrupo) 
            for grupo in response
        ]

    def find_all_without_special_characters(self):
        
        response = self.repo.find_all_without_special_characters()
        
        if not response:
            raise NotFoundException
        
        return [
            GetGrupo(idgrupo=grupo.idgrupo, nmgrupo=grupo.nmgrupo) 
            for grupo in response
        ]
