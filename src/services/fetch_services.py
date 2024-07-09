from src.database.sql_operator import SQLOperator
from datetime import datetime
from typing import List, Dict
from math import floor, ceil



        
        
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

        stock_response = SQLOperator().execute_query(stock_query, tuple(product_ids))
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
        orders_response = SQLOperator().execute_query(order_info_query, tuple(product_ids))
        mapped_orders = {order['iddetalhe']: order['qtpedida'] for order in orders_response}
        return mapped_orders

class DocumentInfoBuilder:
    
    @staticmethod
    def fetch_document_info(product_ids: List[str]) -> dict:
        
        if not product_ids:
            return {}
        
        doc_info_query = """
            SELECT
    doc.iddocumento,
    doc.dtreferencia,
    doc.dtemissao,
    pes.nmpessoa,
    docitem.iddetalhe
FROM
    wshop.documen AS doc
JOIN
    wshop.docitem AS docitem ON docitem.iddocumento = doc.iddocumento
JOIN
    wshop.pessoas AS pes ON pes.idpessoa = doc.idpessoa
WHERE
    docitem.iddetalhe IN ({})
    AND doc.tpoperacao = 'C'
    AND (docitem.iddetalhe, doc.dtreferencia) IN (
        SELECT
            iddetalhe,
            dtreferencia
        FROM
            (
                SELECT
                    di.iddetalhe,
                    di.dtreferencia,
                    ROW_NUMBER() OVER (PARTITION BY di.iddetalhe ORDER BY di.dtreferencia DESC) AS rn
                FROM
                    wshop.documen AS d
                JOIN
                    wshop.docitem AS di ON d.iddocumento = di.iddocumento
                WHERE
                    di.iddetalhe IN ({})
                    AND d.tpoperacao = 'C'
            ) AS ranked
        WHERE
            rn <= 3
    )
    ORDER BY
        docitem.iddetalhe,
        doc.dtreferencia DESC;

        """
        formated_ids = ','.join(['%s'] * len(product_ids))
        doc_info_query = doc_info_query.format(formated_ids, formated_ids)
        doc_info_results = SQLOperator().execute_query(doc_info_query, tuple(product_ids + product_ids))
        doc_info_map = {}
        for doc_info in doc_info_results:
            if doc_info_map.get(doc_info['iddetalhe']):
                doc_info_map[doc_info['iddetalhe']].append(doc_info)
                continue
            doc_info_map[doc_info['iddetalhe']] = []
            doc_info_map[doc_info['iddetalhe']].append(doc_info)
        
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
        sales_result = SQLOperator().execute_query(sales_query.format(formated_ids), product_ids)
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
            else:
                dtref = dtref[0]
            this_prod_sales = [sale['qtvenda'] for sale in sales_info if sale['qtvenda']]
            this_prod_sales_date = [sale['dtreferencia'] for sale in sales_info if sale['qtvenda']]
            all_sales_date = sorted(this_prod_sales_date, reverse=True)
            last_sale = all_sales_date[0].strftime('%d/%m/%Y') if all_sales_date else None
            top_3_sales = sum(list(sorted(this_prod_sales, key=lambda sale: sale, reverse=True))[:5]) / 5
            period_sales =  [sale for sale in sales_info if sale['dtreferencia'] >= dtref]
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
        payment_flux_result = SQLOperator().execute_query(payment_flux_query.format(formated_ids), document_ids)
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
        document_ids = [doc[0]['iddocumento'] for doc in doc_info_map.values()]
        valid_products = SalesUpdate.filter_valid_products(products, doc_info_map)
        products_orders = OrderInfoBuilder.fetch_order_info(product_ids)
        payment_fluxes = PaymentFluxFetcher.fetch_payment_flux(document_ids)
        dtreferencias = {}
        for doc_list in doc_info_map.values():
            for doc in doc_list:
                if doc.get('dtreferencia'):
                    if dtreferencias.get(doc['iddetalhe']):
                        dtreferencias[doc['iddetalhe']].append(doc['dtreferencia'])
                        continue
                    dtreferencias[doc['iddetalhe']] = []
                    dtreferencias[doc['iddetalhe']].append(doc['dtreferencia'])
        
        sales_quants = SalesCalculator.calculate_sales(product_ids, dtreferencias)

        updated_products = [
            SalesUpdate.update_product(
                prod, doc_info_map, payment_fluxes, sales_quants, 
                products_orders, dtreferencias
            )
            for prod in valid_products
        ]


        updated_products.sort(key=lambda x: datetime.strptime(x['dtreferencia'], '%d/%m/%Y'), reverse=True)

        return updated_products

    @staticmethod
    def filter_valid_products(products: List[dict], doc_info_map: Dict) -> List[dict]:
        return [prod for prod in products if prod['iddetalhe'] in doc_info_map.keys()]

    @staticmethod
    def update_product(
            prod: dict, 
            doc_info_map: Dict, 
            payment_fluxes: Dict, 
            sales_quants: Dict, 
            products_orders: Dict,
            dtreferencias: Dict[str, List[datetime]]
        ) -> dict:
        product_id = prod['iddetalhe']
        doc_info = doc_info_map.get(product_id)[0]
        dtreferencia = dtreferencias.get(product_id)
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

     
  
        nmfornecedor = doc_info['nmpessoa']

        calc_durames_response = SalesUpdate.calculate_dura_mes(prod, sales_quant, last_sale_date, dtreferencia)
        dura_mes = calc_durames_response[0]
        dtreferencia = calc_durames_response[1]
        sales_days = calc_durames_response[2]
        shipping_days = 7
        prod['dura_mes'] = dura_mes
        prazo = SalesUpdate.calculate_prazo(payment_flux)

        prod.update({
            'dtreferencia': dtreferencia.strftime('%d/%m/%Y'),
            'sales': sales_quant,
            'shipping_days': shipping_days,
            'supplier': nmfornecedor,
            'stock_min': SalesUpdate.calculate_stock_min(high_avg, sales_quant, shipping_days, sales_days),
            'sugestion': SalesUpdate.calculate_sugestion(sales_quant, prod['dura_mes'], shipping_days, sales_days)
        })
        prod['stock_max'] = SalesUpdate.calculate_stock_max(prod['stock_min'], sales_quant, sales_days)
        prod['sugestion'] = floor(prod['sugestion'])
        
        if prod['qtestoque'] < prod['stock_min']:
            prod['sugestion'] = prod['stock_max'] - prod['qtestoque']

        if prod['qtestoque'] >= prod['stock_max']:
            prod['sugestion'] = 0
        
        if sales_quant and sales_days > 0:
            prod['dura_mes'] = (prod['qtestoque'] > prod['sugestion'])

        prod['sugestion'] -= product_order

        if prod['qtestoque'] + prod['sugestion']  >= prod['stock_max']:
            prod['sugestion'] = prod['stock_max'] - prod['qtestoque']
        
        prod['dura_mes'] = True if prod['sugestion'] <= 0 else False
        prod['sugestion'] = 0 if prod['sugestion'] < 0 else prod['sugestion']
        return prod

    @staticmethod
    def calculate_dura_mes(prod: dict, sales_quant: int, last_sale_date: datetime, dtreferencia: List[datetime]) -> List:
        
        sales_days = 0
        for date in dtreferencia: 
            sales_days = (last_sale_date - date).days if prod['qtestoque'] <= 0 else (datetime.now() - date).days
            if sales_days >= 7:
                break
        dura_mes = bool(sales_days <= 0 or (prod['qtestoque'] > ((sales_quant / sales_days) * 55)))
        
        if not sales_quant:
            dura_mes = True
        
        return [dura_mes, date, sales_days]

    @staticmethod
    def calculate_prazo(payment_flux: list) -> list:
        if payment_flux:
            return [(payment['dtvencimento'] - payment['dtemissao']).days for payment in payment_flux]
        return 'N/A'

    @staticmethod
    def calculate_sugestion(sales_quant: int, dura_mes: bool, shipping_days, sales_days) -> float:
        if dura_mes:
            return 0 
        daily_avg = (sales_quant / sales_days) * 0.75
        return daily_avg * (55 + shipping_days)
    
    @staticmethod
    def calculate_stock_min(high_avg: float, sales_quant: int, shipping_days: int, sales_days) -> int:
        try:
            
            daily_avg = (sales_quant / sales_days) * 0.75
            possible_delay = 1.8
            quotation_period = 2
            reposition_period = ceil(shipping_days * possible_delay + quotation_period)  
            return int(high_avg + daily_avg * reposition_period if sales_days > 0 else high_avg)
        except ZeroDivisionError:
            return high_avg

    @staticmethod
    def calculate_stock_max(stock_min: int, sales_quant: int, sales_days) -> int:
        try:

            daily_avg = (sales_quant / sales_days) * 0.75
            stock_max = stock_min + daily_avg * 55
            return max(3, int(stock_max))

        except ZeroDivisionError:
            return 3

