from datetime import datetime
import json
import re
from typing import List
from auth.database import database_auth

class DatabaseHandler:
    @staticmethod
    def execute_query(query):
        with database_auth() as connection:
            connection.connect()
            response = connection.execute_query(query)
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
        updated_products = []
        stock_query = "SELECT qtestoque FROM wshop.estoque WHERE iddetalhe = '{}' ORDER BY dtreferencia DESC LIMIT 1"

       
        for product in products:
            product_id = product['iddetalhe']
            stock_response = DatabaseHandler.execute_query(stock_query.format(product_id))

            if stock_response:
                stock_quantity = stock_response[0]['qtestoque']
                product['qtestoque'] = stock_quantity
                updated_products.append(product)

        return updated_products

class DocumentInfoFetcher:
    @staticmethod
    def fetch_document_info(product_id):
        doc_info_query = """
            SELECT doc.iddocumento, doc.dtreferencia, doc.dtemissao, pes.nmpessoa 
            FROM wshop.documen AS doc
            JOIN wshop.docitem AS docitem ON docitem.iddocumento = doc.iddocumento
            JOIN wshop.pessoas AS pes ON pes.idpessoa = doc.idpessoa 
            WHERE docitem.iddetalhe = '{}'
            AND doc.tpoperacao = 'C'
            ORDER BY doc.dtreferencia DESC
            LIMIT 1;
        """
        doc_info_result = DatabaseHandler.execute_query(doc_info_query.format(product_id))
        return doc_info_result[0] if doc_info_result else None

class SalesCalculator:
    @staticmethod
    def calculate_sales(product_id, dtreferencia):
        sales_query = """
            SELECT COALESCE(SUM(qtvenda), 0) as total FROM wshop.estoque
            WHERE iddetalhe = '{}'
            AND dtreferencia BETWEEN '{}' AND CURRENT_DATE
        """
        sales_result = DatabaseHandler.execute_query(sales_query.format(product_id, dtreferencia))
        return sales_result[0]['total'] if sales_result else 0

class PaymentFluxFetcher:
    @staticmethod
    def fetch_payment_flux(document_id):
        payment_flux_query = """
            SELECT dtemissao, dtvencimento FROM wshop.fluxo
            WHERE iddocumento = '{}'
        """
        payment_flux_result = DatabaseHandler.execute_query(payment_flux_query.format(document_id))
        return payment_flux_result

class SalesUpdate:
    @staticmethod
    def join_product_sales(products: List[dict]) -> List[dict]:
        updated_products = []
        for prod in products:
            product_id = prod['iddetalhe']
            doc_info = DocumentInfoFetcher.fetch_document_info(product_id)
            if not doc_info:
                continue
            
            dtreferencia = doc_info['dtreferencia']
            dtemissao = doc_info['dtemissao']
            document_id = doc_info['iddocumento']
            nmfornecedor = doc_info['nmpessoa']
            
            shipping_days = (dtreferencia - dtemissao).days
            sales_quant = SalesCalculator.calculate_sales(product_id, dtreferencia)
            payment_flux = PaymentFluxFetcher.fetch_payment_flux(document_id)
            
            prazo = [(payment['dtvencimento'] - payment['dtemissao']).days for payment in payment_flux]
            
            prod['dtreferencia'] = dtreferencia.strftime('%d/%m/%Y')
            prod['sales'] = sales_quant
            prod['shipping_days'] = shipping_days
            prod['supplier'] = nmfornecedor
            prod['payment'] = '/'.join(map(str, prazo))
            
            updated_products.append(prod)
        
        updated_products.sort(key= lambda x : datetime.strptime(x['dtreferencia'], '%d/%m/%Y'), reverse=True)
        
        return updated_products