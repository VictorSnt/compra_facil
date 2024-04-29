import json
from auth.database import database_auth

def fetch_all_prod_family():
    connection = database_auth()
    connection.connect()
    query = "SELECT idfamilia, dsfamilia FROM wshop.familia"
    response = connection.execute_query(query)
    connection.close_connection()
    return response

def fetch_all_prod_groups():
    connection = database_auth()
    connection.connect()
    query = "select idgrupo, nmgrupo from wshop.grupo"
    response = connection.execute_query(query)
    connection.close_connection()
    return response

def fetch_all_prods():
    connection = database_auth()
    connection.connect()
    query = "select iddetalhe, dsdetalhe from wshop.detalhe where stdetalheativo = true"
    response = connection.execute_query(query)
    connection.close_connection()
    return response

def parse_selected_items(selected_items):
    return [json.loads(d.replace("'",'"')) for d in selected_items]

def build_query(groups, families):
    group_values = ",".join([f"'{g['idgrupo']}'" for g in groups])
    family_values = ",".join([f"'{f['idfamilia']}'" for f in families])

    group_filter = f'prod.idgrupo in ({group_values})'
    families_filter = f'det.idfamilia in ({family_values})'
    
    prod_filter = f'{group_filter} or {families_filter}' if groups and families else group_filter if groups else families_filter

    select_all = 'SELECT det.iddetalhe, det.cdprincipal, det.dsdetalhe from wshop.detalhe as det'
    join = 'JOIN wshop.produto as prod on prod.idproduto = det.idproduto'
    where = 'WHERE stdetalheativo = true AND'

    return f'{select_all} {join} {where} {prod_filter}'

def filter_products(data):
    products = data['selectedProds']
    groups = parse_selected_items(data['selectedGroups'])
    families = parse_selected_items(data['selectedFamilies'])
    
    query = build_query(groups, families)
    print(query)
    connection = database_auth()
    connection.connect()
    response = connection.execute_query(query)
    connection.close_connection()
    
    return response
