#std
from typing import List
#ext
from fastapi import APIRouter, Query, Depends
#app
from src.factory.group_service_factory import GroupServiceFactory
from src.schemas.group_schema import GetGroup
from src.services.group_services import GroupService



class GroupController:

    router = APIRouter(prefix='/group')

    @staticmethod
    @router.get('/', response_model=List[GetGroup])
    def get_grupos(
        service: GroupService = Depends(
            GroupServiceFactory.build_default_service
        )):

        return service.find_all()

    @staticmethod
    @router.get('/sem_@', response_model=List[GetGroup])
    def get_without_special_characters(
        service: GroupService = Depends(
        GroupServiceFactory.build_default_service),
        ids: List[str] = Query(None)):

        return service.find_all_without_special_characters(ids)

    @classmethod
    def get_router(cls):
        return cls.router
