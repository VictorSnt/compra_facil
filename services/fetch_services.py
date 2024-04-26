from auth.database import database_auth


def fetch_all_prod_family():
    
    conecction = database_auth()
    conecction.connect()
    query = "SELECT idfamilia, dsfamilia FROM wshop.familia"
    response = conecction.execute_query(query)
    conecction.close_connection()
    return response

def fetch_all_prod_groups():
    
    conecction = database_auth()
    conecction.connect()
    query = "select idgrupo, nmgrupo from wshop.grupo"
    response = conecction.execute_query(query)
    conecction.close_connection()
    return response

def fetch_all_prods():
    
    conecction = database_auth()
    conecction.connect()
    query = "select iddetalhe, dsdetalhe from wshop.detalhe where stdetalheativo = true"
    response = conecction.execute_query(query)
    conecction.close_connection()
    return response

