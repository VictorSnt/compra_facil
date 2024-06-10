from typing import Dict, List, Any
from Configuration.DbConection.queries import get_families, get_groups, get_suppliers
from auth.database import DatabaseHandler


class ProductFinder:
    
    def fetch_all_prod_family(self):
        query = get_families
        data = DatabaseHandler().execute_query(query)
        return self.__remove_all_commas(data, 'dsfamilia')
        

    def fetch_all_prod_groups(self):
        query = get_groups
        data = DatabaseHandler().execute_query(query)
        return self.__remove_all_commas(data, 'nmgrupo')

    def fetch_all_suppliers(self):
        query = get_suppliers 
        data = DatabaseHandler().execute_query(query)
        return data 

    def __remove_all_commas(self, iterable: List[Dict[str, str|Any]], iterable_key: str):
        for data in iterable:
            data[iterable_key] = data[iterable_key].replace("'",'')
        return iterable
