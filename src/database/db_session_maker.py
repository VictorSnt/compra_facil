from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


load_dotenv()
class SessionMaker:

    @classmethod
    def alterdata_session(cls) -> Session:

        ALTERDATA_DB_URI = getenv('ALTERDATA_DB_URI', '')
        engine = create_engine(ALTERDATA_DB_URI)
        new_session = sessionmaker(bind=engine)
        session = new_session()
        return session

    @classmethod
    def own_db_session(cls) -> Session:

        WEBSITE_DB_URI = getenv('WEBSITE_DB_URI', '')
        engine = create_engine(WEBSITE_DB_URI)
        new_session = sessionmaker(bind=engine)
        session = new_session()
        return session

        