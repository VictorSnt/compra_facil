from auth.database import database_auth

conn = database_auth()

conn.connect()

vendedor = '000054'
ini = '2023/05/01'
end = '2023/05/30'

sales_query = """
    SELECT COALESCE(
        (SELECT SUM(item.vlmovimento)
        FROM wshop.docitem AS item
        JOIN wshop.documen AS doc ON item.iddocumento = doc.iddocumento
        JOIN wshop.comitem AS com ON com.iddocitem = item.iddocumentoitem
        JOIN wshop.pessoas AS pes ON com.idpessoa = pes.idpessoa
        WHERE pes.cdchamada = '{}'
        AND doc.stdocumentocancelado != '*'
        AND doc.iddocestorno = ''
        AND doc.tpoperacao = 'V'
        AND doc.dtemissao between '{}' and '{}'), 0)
    -
        COALESCE((SELECT SUM(item.vlmovimento)
        FROM wshop.docitem AS item
        JOIN wshop.documen AS doc ON item.iddocumento = doc.iddocumento
        JOIN wshop.comitem AS com ON com.iddocitem = item.iddocumentoitem
        JOIN wshop.pessoas AS pes ON com.idpessoa = pes.idpessoa
        WHERE pes.cdchamada = '{}'
        AND doc.stdocumentocancelado != '*'
        AND doc.iddocestorno = ''
        AND doc.tpoperacao = 'E'
        AND doc.dtemissao between '{}' and '{}'), 0) 
     AS total
"""

frete_sales = """
        SELECT doc.iddocumento
        FROM wshop.docitem AS item
        JOIN wshop.documen AS doc ON item.iddocumento = doc.iddocumento
        JOIN wshop.comitem AS com ON com.iddocitem = item.iddocumentoitem
        JOIN wshop.pessoas AS pes ON com.idpessoa = pes.idpessoa
        WHERE pes.cdchamada = '{}'
        AND doc.stdocumentocancelado != '*'
        AND doc.iddocestorno = ''
        AND doc.tpoperacao = 'V'
        AND doc.dtemissao between '{}' and '{}'), 0)
"""

frete_sum = """
SELECT SUM(vltotal - vlfrete)  FROM wshop.documen
WHERE iddocumento in ({})
"""
