from fastapi import APIRouter

from src.repository.person_repository import PersonRepository
from src.exceptions.err import NotFoundException
from src.schemas.person_schema import GetPerson


router = APIRouter()


class PersonService:
    
    def __init__(self, repository: PersonRepository) -> None:
        self.repo = repository
    
    def find_all(self):
        
        response = self.repo.find_all()
        
        if not response:
            raise NotFoundException
        
        return [
            GetPerson(id=person.idpessoa, name=person.nmpessoa) 
            for person in response if person
        ]

    def find_all_suppliers(self):
        
        response = self.repo.find_all_suppliers()
        
        if not response:
            raise NotFoundException
        
        return [
            GetPerson(id=person.idpessoa, name=person.nmpessoa) 
            for person in response
        ]
