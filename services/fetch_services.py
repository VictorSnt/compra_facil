from datetime import datetime
from math import floor
from typing import List
from auth.database import database_auth
import json
import re


class DatabaseHandler:
    @staticmethod
    def execute_query(query, args=None):
        with database_auth() as connection:
            connection.connect()
            response = connection.execute_query(query, args)
            connection.close_connection()
        return response

class ProductFetcher:
    @staticmethod
    def fetch_all_prod_family():
        return DatabaseHandler.execute_query("SELECT idfamilia, dsfamilia FROM wshop.familia")

    @staticmethod
    def fetch_all_prod_groups():
        return DatabaseHandler.execute_query("SELECT idgrupo, nmgrupo FROM wshop.grupo")

    @staticmethod
    def fetch_all_prods():
        return DatabaseHandler.execute_query("SELECT iddetalhe, dsdetalhe FROM wshop.detalhe WHERE stdetalheativo = true")

class DataParser:
    @staticmethod
    def parse_selected_items(selected_items):
        parsed_items = []
        for item in selected_items:
            try:
                json_format = item.replace("'", '"')
                parsed_item = json.loads(json_format)
                parsed_items.append(parsed_item)
            except json.JSONDecodeError:
                regex = r'("[^"]*")([^"]*")'
                json_corrected = re.sub(regex, r'\1', json_format)
                input(json_corrected)
                parsed_item = json.loads(json_corrected)
                parsed_items.append(parsed_item)
        return parsed_items

class ProductQueryBuilder:
    @staticmethod
    def build_products_query(groups, families):
        group_values = ",".join([f"'{g['idgrupo']}'" for g in groups])
        family_values = ",".join([f"'{f['idfamilia']}'" for f in families])

        group_filter = f'prod.idgrupo in ({group_values})'
        families_filter = f'det.idfamilia in ({family_values})'
        
        prod_filter = f'{group_filter} or {families_filter}' if groups and families else group_filter if groups else families_filter

        select_all = 'SELECT det.iddetalhe, det.cdprincipal, det.dsdetalhe from wshop.detalhe as det'
        join = 'JOIN wshop.produto as prod on prod.idproduto = det.idproduto'
        where = 'WHERE stdetalheativo = true AND'

        return f'{select_all} {join} {where} {prod_filter}'

class ProductFilter:
    @staticmethod
    def filter_products(data):
        groups = DataParser.parse_selected_items(data['selectedGroups'])
        families = DataParser.parse_selected_items(data['selectedFamilies'])
        
        query = ProductQueryBuilder.build_products_query(groups, families)
        return DatabaseHandler.execute_query(query)

class StockUpdater:
    @staticmethod
    def join_products_stock(products: List[dict]) -> List[dict]:
        if not products:
            return []

        # Coleta todos os ids de detalhes dos produtos
        product_ids = [product['iddetalhe'] for product in products]

        # Consulta SQL para obter o estoque mais recente de cada detalhe
        stock_query = """
        SELECT e.iddetalhe, e.qtestoque
        FROM wshop.estoque e
        INNER JOIN (
            SELECT iddetalhe, MAX(dtreferencia) AS max_dtreferencia
            FROM wshop.estoque
            GROUP BY iddetalhe
        ) AS latest_stock ON e.iddetalhe = latest_stock.iddetalhe AND e.dtreferencia = latest_stock.max_dtreferencia
        WHERE e.iddetalhe IN ({})
        """.format(','.join(['%s'] * len(product_ids)))

        # Executa a consulta com todos os ids de detalhes dos produtos
        stock_response = DatabaseHandler.execute_query(stock_query, tuple(product_ids))

        # Mapeia as respostas de estoque para um dicionário com os ids de detalhe como chave
        stock_map = {stock['iddetalhe']: stock['qtestoque'] for stock in stock_response}

        # Atualiza os produtos com as informações de estoque correspondentes
        updated_products = []
        for product in products:
            stock_quantity = stock_map.get(product['iddetalhe'])
            if stock_quantity is not None:
                product['qtestoque'] = stock_quantity
                updated_products.append(product)

        return updated_products

class DocumentInfoFetcher:
    @staticmethod
    def fetch_document_info(product_ids: List[str]) -> dict:
        
        if not product_ids:
            return {}
        
        doc_info_query = """
            SELECT doc.iddocumento, doc.dtreferencia, doc.dtemissao, pes.nmpessoa, docitem.iddetalhe
            FROM wshop.documen AS doc
            JOIN wshop.docitem AS docitem ON docitem.iddocumento = doc.iddocumento
            JOIN wshop.pessoas AS pes ON pes.idpessoa = doc.idpessoa 
            WHERE (docitem.iddetalhe IN ({}))
            AND doc.tpoperacao = 'C'
            AND (docitem.iddetalhe, doc.dtreferencia) IN (
                SELECT iddetalhe, dtreferencia
                FROM (
                    SELECT di.iddetalhe, di.dtreferencia, 
                        ROW_NUMBER() OVER (PARTITION BY di.iddetalhe ORDER BY di.dtreferencia DESC) AS rn
                    FROM wshop.documen AS d
                    JOIN wshop.docitem AS di ON d.iddocumento = di.iddocumento
                    WHERE di.iddetalhe IN ({})
                    AND d.tpoperacao = 'C'
                ) AS ranked
                WHERE rn = 1
            )
            ORDER BY doc.dtreferencia DESC;
        """
        formated_ids = ','.join(['%s'] * len(product_ids))
        doc_info_query = doc_info_query.format(formated_ids, formated_ids)
        doc_info_results = DatabaseHandler.execute_query(doc_info_query, tuple(product_ids + product_ids))
        doc_info_map = {doc_info['iddetalhe']: doc_info for doc_info in doc_info_results}
        return doc_info_map
    
class SalesCalculator:
    @staticmethod
    def calculate_sales(product_ids, dtreferencias):
        sales_query = """
            SELECT 
                iddetalhe,
                qtvenda,
                dtreferencia
            FROM 
                wshop.estoque
            WHERE 
                iddetalhe IN ({})
            ORDER BY 
                iddetalhe, dtreferencia ASC;
        """
        formated_ids = ','.join(['%s'] * len(product_ids))
        sales_result = DatabaseHandler.execute_query(sales_query.format(formated_ids), product_ids)
        filtered_sales = {}
        for sale in sales_result:
            if not sale['iddetalhe'] in filtered_sales:
                filtered_sales[sale['iddetalhe']] = []
            if not sale['dtreferencia'] in filtered_sales[sale['iddetalhe']]:
                filtered_sales[sale['iddetalhe']].append(
                    {'dtreferencia': sale['dtreferencia'], 'qtvenda': sale['qtvenda']}
                )
        calc_sales = {}
        for iddetalhe, sales_info in filtered_sales.items():
            dtref = dtreferencias.get(iddetalhe)
            if not dtref:
                continue
            period_sales =  [sale for sale in sales_info if sale['dtreferencia'] >= dtreferencias.get(iddetalhe)]
            only_sales = [period['qtvenda'] for period in period_sales if period['qtvenda']]
            calc_sales[iddetalhe] = sum(only_sales)
        return calc_sales

class PaymentFluxFetcher:
    @staticmethod
    def fetch_payment_flux(document_ids):
        payment_flux_query = """
            SELECT dtemissao, dtvencimento, iddocumento FROM wshop.fluxo
            WHERE iddocumento IN ({})
        """
        formated_ids = ','.join(['%s'] * len(document_ids))
        payment_flux_result = DatabaseHandler.execute_query(payment_flux_query.format(formated_ids), document_ids)
        formated_flux = {}
        for flux in payment_flux_result:
            if not flux['iddocumento'] in formated_flux:
                formated_flux[flux['iddocumento']] = []
            formated_flux[flux['iddocumento']].append(flux)
        return formated_flux

class SalesUpdate:
    @staticmethod
    def join_product_sales(products: List[dict]) -> List[dict]:
        if not products:
            return []

        product_ids = [prod['iddetalhe'] for prod in products]
        doc_info_map = DocumentInfoFetcher.fetch_document_info(product_ids)
        products = [
            prod for prod in products if prod['iddetalhe'] in 
            {info['iddetalhe'] for info in doc_info_map.values()}
        ]
        print(datetime.now())
        document_ids = [doc['iddocumento'] for doc in doc_info_map.values()]
        payment_fluxes = PaymentFluxFetcher.fetch_payment_flux(document_ids)
        print(datetime.now())
        dtreferencias = {doc['iddetalhe']: doc['dtreferencia'] for doc in doc_info_map.values()}
        sales_quants = SalesCalculator.calculate_sales(product_ids, dtreferencias)
        print(datetime.now())
        updated_products = []
        
        for prod in products:
            product_id = prod['iddetalhe']
            doc_info = doc_info_map.get(product_id)
            document_id = doc_info['iddocumento']
            payment_flux = payment_fluxes.get(document_id)
            sales_quant = sales_quants.get(product_id)
            if not doc_info:
                continue
            dtreferencia: datetime = doc_info['dtreferencia']
            dtemissao = doc_info['dtemissao']
            document_id = doc_info['iddocumento']
            nmfornecedor = doc_info['nmpessoa']
            prod['dura_mes'] = True
            sales_days = (datetime.now() - dtreferencia).days
            if sales_quant:
                prod['dura_mes'] = (prod['qtestoque'] > ((sales_quant / sales_days) * 30))

            shipping_days = (dtreferencia - dtemissao).days
            if payment_flux:
                prazo = [(payment['dtvencimento'] - payment['dtemissao']).days for payment in payment_flux]
            else:
                prazo = 'N/A'
            prod['dtreferencia'] = dtreferencia.strftime('%d/%m/%Y')
            prod['sales'] = sales_quant
            prod['shipping_days'] = shipping_days
            prod['supplier'] = nmfornecedor
            prod['payment'] = '/'.join(map(str, prazo))
            prod['sugestion'] = (sales_quant / sales_days * 15) if not prod['dura_mes'] else 0
            if prod['sugestion'] > 0 and prod['sugestion'] < 3:
                prod['sugestion'] = 3
            updated_products.append(prod)
            prod['sugestion'] = floor(prod['sugestion'])
        updated_products.sort(key=lambda x: datetime.strptime(x['dtreferencia'], '%d/%m/%Y'), reverse=True)
        updated_products.sort(key=lambda x: x['supplier'])
        return updated_products

