from src.database.sql_operator import SQLOperator


class ProductServices:

    def __init__(self, db: SQLOperator):
        self.db = db

    def join_groups_n_family(self, data):
   
        groups = data['selectedGroups']
        families = data['selectedFamilies']
        groups_ids = self.db.format_to_sql(groups, 'idgrupo')
        families_ids = self.db.format_to_sql(families, 'idfamilia')
        query = self.db.build_products_query(groups_ids, families_ids)
        return self.db.execute_query(query) or []

    
    def join_suppliers(self, data):
        
        suppliers = data['selectedSuppliers']
        sup_ids_string = self.db.format_to_sql(suppliers, 'idpessoa')
        query = self.db.build_suppliers_query(sup_ids_string)
        return self.db.execute_query(query) or []
    