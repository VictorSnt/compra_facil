from auth.database import DatabaseHandler
from services.jsonifier import Jsonyfier
from datetime import datetime
from typing import List, Dict
from math import floor, ceil


class ProductFilter:
    @staticmethod
    def filter_by_family_n_groups(data):
        
        groups = Jsonyfier.parse(data['selectedGroups'])
        families = Jsonyfier.parse(data['selectedFamilies'])
        query = ProductFilter.build_products_query(groups, families)
        return DatabaseHandler().execute_query(query) or []

    @staticmethod
    def filter_by_suppliers(data):
        suppliers = Jsonyfier.parse(data['selectedSuppliers'])
        sup_ids_string = ",".join([f"'{sup['idpessoa']}'" for sup in suppliers])
        query = ProductFilter.build_supplied_by_query(sup_ids_string)
        return DatabaseHandler().execute_query(query) or []

    @staticmethod
    def build_products_query(groups, families):
        group_values = ",".join([f"'{g['idgrupo']}'" for g in groups if groups])
        print(groups)
        print(families)
        family_values = ",".join([f"'{f['idfamilia']}'" for f in families if families])

        group_filter = f'prod.idgrupo in ({group_values})'
        families_filter = f'det.idfamilia in ({family_values})'
        
        prod_filter = f'{group_filter} or {families_filter}' if groups and families else group_filter if groups else families_filter

        select_all = 'SELECT det.iddetalhe, det.cdprincipal, det.dsdetalhe from wshop.detalhe as det'
        join = 'JOIN wshop.produto as prod on prod.idproduto = det.idproduto'
        where = 'WHERE stdetalheativo = true AND'

        return f'{select_all} {join} {where} {prod_filter}'
    
    def build_supplied_by_query(ids):
        query = """
        SELECT DISTINCT det.iddetalhe, det.cdprincipal, det.dsdetalhe FROM wshop.docitem as item
        JOIN wshop.detalhe as det on det.iddetalhe = item.iddetalhe
        JOIN wshop.documen as doc on doc.iddocumento = item.iddocumento
        WHERE doc.idpessoa IN ({})  AND det.stdetalheativo = TRUE
        """
        return query.format(ids) 
    
class StockUpdater:
    @staticmethod
    def join_products_stock(products: List[dict]) -> List[dict]:
        if not products:
            return []

        product_ids = [product['iddetalhe'] for product in products]
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

        stock_response = DatabaseHandler().execute_query(stock_query, tuple(product_ids))
        stock_map = {stock['iddetalhe']: stock['qtestoque'] for stock in stock_response}
        updated_products = []
        for product in products:
            stock_quantity = stock_map.get(product['iddetalhe'])
            if stock_quantity is not None:
                product['qtestoque'] = stock_quantity
                updated_products.append(product)

        return updated_products

class OrderInfoBuilder:

    @staticmethod
    def fetch_order_info(product_ids: List[str]) -> dict:
        
        if not product_ids:
            return {}

        order_info_query = """
            SELECT pitem.iddetalhe, pitem.qtpedida FROM wshop.pedidos AS ped
            JOIN wshop.peditem AS pitem ON ped.idpedido = pitem.idpedido
            WHERE ped.cdstatus = 'Aberto' AND pitem.iddetalhe IN ({})
        """.format(','.join(['%s'] * len(product_ids)))
        orders_response = DatabaseHandler().execute_query(order_info_query, tuple(product_ids))
        mapped_orders = {order['iddetalhe']: order['qtpedida'] for order in orders_response}
        return mapped_orders

class DocumentInfoBuilder:
    
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
        doc_info_results = DatabaseHandler().execute_query(doc_info_query, tuple(product_ids + product_ids))
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
        sales_result = DatabaseHandler().execute_query(sales_query.format(formated_ids), product_ids)
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
            this_prod_sales = [sale['qtvenda'] for sale in sales_info if sale['qtvenda']]
            this_prod_sales_date = [sale['dtreferencia'] for sale in sales_info if sale['qtvenda']]
            all_sales_date = sorted(this_prod_sales_date, reverse=True)
            last_sale = all_sales_date[0].strftime('%d/%m/%Y') if all_sales_date else None
            top_3_sales = sum(list(sorted(this_prod_sales, key=lambda sale: sale, reverse=True))[:5]) / 5
            period_sales =  [sale for sale in sales_info if sale['dtreferencia'] >= dtreferencias.get(iddetalhe)]
            only_sales = [period['qtvenda'] for period in period_sales if period['qtvenda']]
            calc_sales[iddetalhe] = {'total_sales': sum(only_sales), 'high_avg': top_3_sales, 'last_sale' :last_sale}
        return calc_sales

class PaymentFluxFetcher:
    @staticmethod
    def fetch_payment_flux(document_ids):
        payment_flux_query = """
            SELECT dtemissao, dtvencimento, iddocumento FROM wshop.fluxo
            WHERE iddocumento IN ({})
        """
        formated_ids = ','.join(['%s'] * len(document_ids))
        payment_flux_result = DatabaseHandler().execute_query(payment_flux_query.format(formated_ids), document_ids)
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
        doc_info_map = DocumentInfoBuilder.fetch_document_info(product_ids)
        document_ids = [doc['iddocumento'] for doc in doc_info_map.values()]
        valid_products = SalesUpdate.filter_valid_products(products, doc_info_map)
        products_orders = OrderInfoBuilder.fetch_order_info(product_ids)
        payment_fluxes = PaymentFluxFetcher.fetch_payment_flux(document_ids)
        dtreferencias = {doc['iddetalhe']: doc['dtreferencia'] for doc in doc_info_map.values()}
        sales_quants = SalesCalculator.calculate_sales(product_ids, dtreferencias)

        updated_products = [
            SalesUpdate.update_product(prod, doc_info_map, payment_fluxes, sales_quants, products_orders) 
            for prod in valid_products
        ]


        updated_products.sort(key=lambda x: datetime.strptime(x['dtreferencia'], '%d/%m/%Y'), reverse=True)

        return updated_products

    @staticmethod
    def filter_valid_products(products: List[dict], doc_info_map: Dict) -> List[dict]:
        return [prod for prod in products if prod['iddetalhe'] in doc_info_map]

    @staticmethod
    def update_product(prod: dict, doc_info_map: Dict, payment_fluxes: Dict, sales_quants: Dict, products_orders: Dict) -> dict:
        product_id = prod['iddetalhe']
        doc_info = doc_info_map.get(product_id)

        if not doc_info:
            return prod
       
        document_id = doc_info['iddocumento']
        payment_flux = payment_fluxes.get(document_id)
        product_order = products_orders.get(product_id, 0)
        sales_info = sales_quants.get(product_id, {})
        sales_quant = sales_info.get('total_sales')
        high_avg = sales_info.get('high_avg')
        prod['last_sale'] = sales_info.get('last_sale')
        last_sale_date = datetime.strptime(prod['last_sale'], '%d/%m/%Y') if prod['last_sale'] else datetime.now()

        dtreferencia = doc_info['dtreferencia']
        dtemissao = doc_info['dtemissao']
        nmfornecedor = doc_info['nmpessoa']

        prod['dura_mes'] = SalesUpdate.calculate_dura_mes(prod, sales_quant, last_sale_date, dtreferencia)
        shipping_days = 7
        prazo = SalesUpdate.calculate_prazo(payment_flux)

        prod.update({
            'dtreferencia': dtreferencia.strftime('%d/%m/%Y'),
            'sales': sales_quant,
            'shipping_days': shipping_days,
            'supplier': nmfornecedor,
            'stock_min': SalesUpdate.calculate_stock_min(prod, high_avg, sales_quant, shipping_days, last_sale_date, dtreferencia),
            'sugestion': SalesUpdate.calculate_sugestion(sales_quant, prod['dura_mes'], prod, last_sale_date, dtreferencia, shipping_days)
        })
        prod['stock_max'] = SalesUpdate.calculate_stock_max(prod, prod['stock_min'], sales_quant, last_sale_date, dtreferencia)
        prod['sugestion'] = floor(prod['sugestion'])
        
        if prod['qtestoque'] < prod['stock_min']:
            prod['sugestion'] = prod['stock_max'] - prod['qtestoque']

        if prod['qtestoque'] >= prod['stock_max']:
            prod['sugestion'] = 0
        
        sales_days = (last_sale_date - dtreferencia).days if prod['qtestoque'] <= 0 else (datetime.now() - dtreferencia).days
        if sales_quant and sales_days > 0:
            prod['dura_mes'] = (prod['qtestoque'] > prod['sugestion'])

        prod['sugestion'] -= product_order

        if prod['qtestoque'] + prod['sugestion']  >= prod['stock_max']:
            prod['sugestion'] = prod['stock_max'] - prod['qtestoque']
        
        prod['dura_mes'] = True if prod['sugestion'] <= 0 else False
        prod['sugestion'] = 0 if prod['sugestion'] < 0 else prod['sugestion']
        return prod

    @staticmethod
    def calculate_dura_mes(prod: dict, sales_quant: int, last_sale_date: datetime, dtreferencia: datetime) -> bool:
        if not sales_quant:
            return True
        sales_days = (last_sale_date - dtreferencia).days if prod['qtestoque'] <= 0 else (datetime.now() - dtreferencia).days 
        return sales_days <= 0 or (prod['qtestoque'] > ((sales_quant / sales_days) * 55))

    @staticmethod
    def calculate_prazo(payment_flux: list) -> list:
        if payment_flux:
            return [(payment['dtvencimento'] - payment['dtemissao']).days for payment in payment_flux]
        return 'N/A'

    @staticmethod
    def calculate_sugestion(sales_quant: int, dura_mes: bool, prod, last_sale_date, dtreferencia, shipping_days) -> float:
        if dura_mes:
            return 0
        sales_days = (last_sale_date - dtreferencia).days if prod['qtestoque'] <= 0 else (datetime.now() - dtreferencia).days 
        daily_avg = (sales_quant / sales_days) * 0.75
        return daily_avg * (55 + shipping_days)
    
    @staticmethod
    def calculate_stock_min(
            prod, high_avg: float, sales_quant: int, shipping_days: int, 
            last_sale_date: datetime, dtreferencia: datetime
        ) -> int:
        try:
            sales_days = (last_sale_date - dtreferencia).days if prod['qtestoque'] <= 0 else (datetime.now() - dtreferencia).days 
            daily_avg = (sales_quant / sales_days) * 0.75
            possible_delay = 1.8
            quotation_period = 2
            reposition_period = ceil(shipping_days * possible_delay + quotation_period)  
            return int(high_avg + daily_avg * reposition_period if sales_days > 0 else high_avg)
        except ZeroDivisionError:
            return high_avg

    @staticmethod
    def calculate_stock_max(prod, stock_min: int, sales_quant: int, last_sale_date: datetime, dtreferencia: datetime) -> int:
        try:
            sales_days = (last_sale_date - dtreferencia).days if prod['qtestoque'] <= 0 else (datetime.now() - dtreferencia).days 
            daily_avg = (sales_quant / sales_days) * 0.75
            stock_max = stock_min + daily_avg * 55
            return max(3, int(stock_max))
        except ZeroDivisionError:
            return 3

