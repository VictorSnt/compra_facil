#ext
from fastapi import Depends
from sqlalchemy.orm import Session
#app
from src.database.db_session_maker import SessionMaker
from src.model.group import Group
from src.repository.group_repository import GroupRepository
from src.services.group_services import GroupService


class GroupServiceFactory:
    
    @classmethod
    def build_default_service(
        cls, session: Session = Depends(SessionMaker.alterdata_session)):
        
        repo = GroupRepository(session, Group)
        return GroupService(repo)