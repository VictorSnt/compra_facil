get_families = """
SELECT 
    idfamilia, dsfamilia 
FROM 
    wshop.familia 
WHERE 
    dsfamilia NOT LIKE '%@%'
"""


get_groups = """
SELECT 
    idgrupo, nmgrupo 
FROM 
    wshop.grupo 
WHERE 
    nmgrupo NOT LIKE '%@%' 
AND 
    nmgrupo NOT LIKE '%*%'
"""


get_suppliers = """
SELECT 
    idpessoa, nmpessoa 
FROM 
    wshop.pessoas
WHERE 
    sttipopessoa = 'F'
ORDER BY 
    nmpessoa 
ASC
"""
