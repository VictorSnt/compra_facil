from typing import List
from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.familia_repository import FamiliaRepository
from src.schemas.familia_schema import GetFamilia

router = APIRouter()


class FamiliaService:
    
    def __init__(self, repository: FamiliaRepository) -> None:
        self.repo = repository
    
    def find_all(self):
        
        response = self.repo.find_all()
        
        if not response:
            raise NotFoundException
        
        return [
            GetFamilia(idfamilia=familia.idfamilia, dsfamilia=familia.dsfamilia) 
            for familia in response
        ]

    def find_all_without_special_characters(self, ids):
        
        response = self.repo.find_all_without_special_characters(ids)
        
        if not response:
            raise NotFoundException
        
        return [
            GetFamilia(idfamilia=familia.idfamilia, dsfamilia=familia.dsfamilia) 
            for familia in response
        ]

    def find_by_id(self, id: str):
        
        response = self.repo.find_by_id(id)
        
        if not response:
            raise NotFoundException
        
        return [
            GetFamilia(idfamilia=familia.idfamilia, dsfamilia=familia.dsfamilia) 
            for familia in response
        ]