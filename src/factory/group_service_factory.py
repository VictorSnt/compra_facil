from fastapi.params import Depends
from sqlalchemy.orm import Session


from src.database.db_session_maker import Session_Maker
from src.model.group import Group
from src.repository.group_repository import GroupRepository
from src.services.group_services import GroupService


class GroupServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = GroupRepository(session, Group)
        return GroupService(repo)