from typing import List
from fastapi import APIRouter, Query
from fastapi.params import Depends

from src.factory.group_service_factory import GroupServiceFactory
from src.schemas.group_schema import GetGroup
from src.services.group_services import GroupService



class GroupController:
    
    router = APIRouter(prefix='/group')
    
    @router.get('/', response_model=List[GetGroup])
    def get_grupos(service: GroupService = Depends(GroupServiceFactory.build_default_Service)):
        
        return service.find_all()

    @router.get('/sem_@', response_model=List[GetGroup])
    def get_without_special_characters(
        service: GroupService = Depends(
        GroupServiceFactory.build_default_Service),
        ids: List[str] = Query(None)):
        
        return service.find_all_without_special_characters(ids)

    @classmethod
    def get_router(cls):
        return cls.router
