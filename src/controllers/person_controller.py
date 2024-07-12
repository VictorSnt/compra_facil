#std
from typing import List
#ext
from fastapi import APIRouter, Query, Depends
#app
from src.factory.person_service_factory import PersonServiceFactory
from src.schemas.person_schema import GetPerson
from src.services.person_service import PersonService



class PersonController:

    router = APIRouter(prefix='/persons')

    @staticmethod
    @router.get('/', response_model=List[GetPerson])
    def get_persons(
        service: PersonService = Depends(
            PersonServiceFactory.build_default_service
        ),
        only_suppliers: bool = Query(False)
        ):

        if only_suppliers:
            return service.find_all_suppliers()
        return service.find_all()

    @classmethod
    def get_router(cls):
        return cls.router
