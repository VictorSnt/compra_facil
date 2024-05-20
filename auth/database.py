from Configuration.DbConection.DbConnect import DbConnection
from dotenv import load_dotenv
from os import getenv


load_dotenv()

class DatabaseHandler:

    
    def database_auth(self) -> DbConnection:
        conecction = DbConnection(
            host=getenv('HOST'),
            port=getenv('PORT'),
            dbname=getenv('DBNAME'),
            user=getenv('USER'),
            password=getenv('PASSWD')
        )
        return conecction

    
    def execute_query(self, query, args=None):
        with self.database_auth() as connection:
            connection.connect()
            response = connection.execute_query(query, args)
            connection.close_connection()
        return response