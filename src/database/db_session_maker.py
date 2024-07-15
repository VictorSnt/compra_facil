from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


load_dotenv()
class SessionMaker:

    @classmethod
    def create_session(cls, quotes_db: bool=False) -> Session:
        if not quotes_db:
            SQLALQUEMY_URI = getenv('SQLALQUEMY_URI')
        else:
            SQLALQUEMY_URI = 'sqlite:///database2.db'
        engine = create_engine(SQLALQUEMY_URI)
        new_session = sessionmaker(bind=engine)
        session = new_session()
        return session
