from typing import List
from fastapi import APIRouter, Path, Query
from fastapi.params import Depends

from src.factory.family_service_factory import FamilyServiceFactory
from src.schemas.family_schema import GetFamily
from src.services.family_service import FamilyService



class FamilyController:
    
    router = APIRouter(prefix='/family')
    
    @classmethod
    @router.get('/', response_model=List[GetFamily])
    def get_familias(service: FamilyService = Depends(FamilyServiceFactory.build_default_Service)):
        
        return service.find_all()
    
    @classmethod
    @router.get('/sem_@', response_model=List[GetFamily])
    def get_without_special_characters(
        service: FamilyService = Depends(FamilyServiceFactory.build_default_Service),
        ids: List[str] = Query(None)):
        
        return service.find_all_without_special_characters(ids)

    @router.get('/{id}', response_model=List[GetFamily])
    def find_by_id(
        service: FamilyService = Depends(
            FamilyServiceFactory.build_default_Service),
        id: str = Path()
        ):
        
        return service.find_by_id(id)
    
    @classmethod
    def get_router(cls):
        return cls.router
