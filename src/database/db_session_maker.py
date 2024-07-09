from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from os import getenv


load_dotenv()
class Session_Maker:

    @classmethod
    def create_session(cls) -> Session:
        SQLALQUEMY_URI = getenv('SQLALQUEMY_URI')
        engine = create_engine(SQLALQUEMY_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
