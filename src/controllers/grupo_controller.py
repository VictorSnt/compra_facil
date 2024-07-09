from typing import List
from fastapi import APIRouter
from fastapi.params import Depends

from src.factory.grupo_service_factory import GrupoServiceFactory
from src.schemas.grupo_schema import GetGrupo
from src.services.grupo_services import GrupoService



class GrupoController:
    
    router = APIRouter(prefix='/grupo')
    
    @router.get('/', response_model=List[GetGrupo])
    def get_grupos(service: GrupoService = Depends(GrupoServiceFactory.build_default_Service)):
        
        return service.find_all()

    @router.get('/sem_@', response_model=List[GetGrupo])
    def get_without_special_characters(service: GrupoService = Depends(GrupoServiceFactory.build_default_Service)):
        
        return service.find_all_without_special_characters()

    @classmethod
    def get_router(cls):
        return cls.router
