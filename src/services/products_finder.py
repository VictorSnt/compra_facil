from src.queries.queries import get_families, get_groups, get_suppliers
from src.database.sql_operator import SQLOperator


class ProductFinder:
    
    def find_all_prod_family(self):
        query = get_families
        data = SQLOperator().execute_query(query)
        return data    

    def find_all_prod_groups(self):
        query = get_groups
        data = SQLOperator().execute_query(query)
        return data


    def find_all_suppliers(self):
        query = get_suppliers 
        data = SQLOperator().execute_query(query)
        return data 
