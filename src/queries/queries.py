get_families = """
SELECT 
    idfamilia, dsfamilia 
FROM 
    wshop.family 
WHERE 
    dsfamilia NOT LIKE '%@%'
ORDER BY dsfamilia ASC
"""


get_groups = """
SELECT 
    idgrupo, nmgrupo 
FROM 
    wshop.group 
WHERE 
    nmgrupo NOT LIKE '%@%' 
AND 
    nmgrupo NOT LIKE '%*%'
    ORDER BY nmgrupo ASC
"""


get_suppliers = """
SELECT 
    idpessoa, nmpessoa 
FROM 
    wshop.Person
WHERE 
    sttipopessoa = 'F'
ORDER BY 
    nmpessoa 
ASC
"""

suplier_query = """
    SELECT DISTINCT det.iddetalhe, det.cdprincipal, det.dsdetalhe FROM wshop.docitem as item
    JOIN wshop.detalhe as det on det.iddetalhe = item.iddetalhe
    JOIN wshop.documen as doc on doc.iddocumento = item.iddocumento
    WHERE doc.idpessoa IN ({})  AND det.stdetalheativo = TRUE
"""