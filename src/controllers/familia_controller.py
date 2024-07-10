from typing import List
from fastapi import APIRouter, Path, Query
from fastapi.params import Depends

from src.factory.familia_service_factory import FamiliaServiceFactory
from src.schemas.familia_schema import GetFamilia
from src.services.familia_service import FamiliaService



class FamiliaController:
    
    router = APIRouter(prefix='/familia')
    
    @classmethod
    @router.get('/', response_model=List[GetFamilia])
    def get_familias(service: FamiliaService = Depends(FamiliaServiceFactory.build_default_Service)):
        
        return service.find_all()
    @classmethod
    @router.get('/sem_@', response_model=List[GetFamilia])
    def get_without_special_characters(
        service: FamiliaService = Depends(FamiliaServiceFactory.build_default_Service),
        ids: List[str] = Query(None)):
        
        return service.find_all_without_special_characters(ids)

    @router.get('/{id}', response_model=List[GetFamilia])
    def find_by_id(
        service: FamiliaService = Depends(
            FamiliaServiceFactory.build_default_Service),
        id: str = Path()
        ):
        
        return service.find_by_id(id)
    
    @classmethod
    def get_router(cls):
        return cls.router
