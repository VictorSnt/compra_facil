from typing import List
from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.family_repository import FamilyRepository
from src.schemas.family_schema import GetFamily

router = APIRouter()


class FamilyService:
    
    def __init__(self, repository: FamilyRepository) -> None:
        self.repo = repository
    
    def find_all(self):
        
        response = self.repo.find_all()
        
        if not response:
            raise NotFoundException
        
        return [
            GetFamily(idfamilia=family.idfamilia, dsfamilia=family.dsfamilia) 
            for family in response
        ]

    def find_all_without_special_characters(self, ids):
        
        response = self.repo.find_all_without_special_characters(ids)
        
        if not response:
            raise NotFoundException
        
        return [
            GetFamily(idfamilia=family.idfamilia, dsfamilia=family.dsfamilia) 
            for family in response
        ]

    def find_by_id(self, id: str):
        
        response = self.repo.find_by_id(id)
        
        if not response:
            raise NotFoundException
        
        return [
            GetFamily(idfamilia=family.idfamilia, dsfamilia=family.dsfamilia) 
            for family in response
        ]