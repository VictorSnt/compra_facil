from src.database.db_connection.db_connect import DbConnection
from src.queries.queries import suplier_query
from typing import Dict, List
from dotenv import load_dotenv
from os import getenv


load_dotenv()

class SQLOperator:

    
    def __get_conn(self) -> DbConnection:
        conecction = DbConnection(
            host=getenv('HOST'),
            port=getenv('PORT'),
            dbname=getenv('DBNAME'),
            user=getenv('USER'),
            password=getenv('PASSWD')
        )
        return conecction

    
    def execute_query(self, query, args=None):
        with self.__get_conn() as connection:
            connection.connect()
            response = connection.execute_query(query, args)
            connection.close_connection()
        return response
    
    def build_suppliers_query(self, ids):
        query = suplier_query
        return query.format(ids)
    
    def build_products_query(self, groups_ids, families_ids):
        
        
        group_filter = f'prod.idgrupo in ({groups_ids})'
        families_filter = f'det.idfamilia in ({families_ids})'
        where_ids = ''
        if groups_ids and families_ids:
            where_ids = f'{group_filter} or {families_filter}'
        elif groups_ids:
            where_ids = group_filter
        else:
            where_ids = families_filter

        select_all = 'SELECT det.iddetalhe, det.cdprincipal, det.dsdetalhe from wshop.detalhe as det'
        join = 'JOIN wshop.product as prod on prod.idproduto = det.idproduto'
        where = 'WHERE stdetalheativo = true AND'

        return f'{select_all} {join} {where} {where_ids}'
    
    
    def format_to_sql(self, data: List[Dict], dict_key: str):
        
        if not data:
            return None
        return ",".join([f"'{d[dict_key]}'" for d in data if data])