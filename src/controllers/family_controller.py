#std
from typing import List
#ext
from fastapi import APIRouter, Query, Depends, Path
#app
from src.factory.family_service_factory import FamilyServiceFactory
from src.schemas.family_schema import GetFamily
from src.services.family_service import FamilyService



class FamilyController:

    router = APIRouter(prefix='/family')

    @staticmethod
    @router.get('/', response_model=List[GetFamily])
    def get_familias(service: FamilyService = Depends(
        FamilyServiceFactory.build_default_service
    )):

        return service.find_all()

    @staticmethod
    @router.get('/sem_@', response_model=List[GetFamily])
    def get_without_special_characters(
        service: FamilyService = Depends(
            FamilyServiceFactory.build_default_service
        ),
        ids: List[str] = Query(None)
    ):

        return service.find_all_without_special_characters(ids)

    @staticmethod
    @router.get('/{id}', response_model=List[GetFamily])
    def find_by_id(
        service: FamilyService = Depends(
            FamilyServiceFactory.build_default_service),
        family_id: str = Path()
    ):

        return service.find_by_id(family_id)

    @classmethod
    def get_router(cls):
        return cls.router
