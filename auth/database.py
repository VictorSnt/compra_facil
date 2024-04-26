from Configuration.DbConection.DbConnect import DbConnection
from dotenv import load_dotenv
from os import getenv


def database_auth() -> DbConnection:
    load_dotenv()
    conecction = DbConnection(
        host=getenv('HOST'),
        port=getenv('PORT'),
        dbname=getenv('DBNAME'),
        user=getenv('USER'),
        password=getenv('PASSWD')
    )
    return conecction