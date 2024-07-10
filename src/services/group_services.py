from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.group_repository import GroupRepository
from src.schemas.group_schema import GetGroup

router = APIRouter()


class GroupService:
    
    def __init__(self, repository: GroupRepository) -> None:
        self.repo = repository
    
    def find_all(self):
        
        response = self.repo.find_all()
        
        if not response:
            raise NotFoundException
        
        return [
            GetGroup(idgrupo=group.idgrupo, nmgrupo=group.nmgrupo) 
            for group in response
        ]

    def find_all_without_special_characters(self, ids):
        
        response = self.repo.find_all_without_special_characters(ids)
        
        if not response:
            raise NotFoundException
        
        return [
            GetGroup(idgrupo=group.idgrupo, nmgrupo=group.nmgrupo) 
            for group in response
        ]
