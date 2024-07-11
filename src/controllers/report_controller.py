from datetime import datetime
from typing import List
from fastapi import APIRouter, Query

from src.database.db_session_maker import Session_Maker
from src.exceptions.err import NotFoundException
from src.repository.product_repository import ProductRepository
from src.model.models import *



class ReportController:
    
    router = APIRouter(prefix="/report")   
    session = Session_Maker.create_session()
    repo = repository = ProductRepository(session, Product, ProductInfo)
        
    @router.get('/shopping_sugestion')
    def shopping_sugestion(
        product_ids: List[str] = Query()
    ):
        retorno = []
        prods = ReportController.repo.find_products_with_current_stock(product_ids)
        for prod in prods:
            stock = prod.latest_stock.qtestoque
            last_purchase = prod.last_relevant_purchase(ReportController.repo.session)
            days_since_last_purchase = (datetime.now() - last_purchase).days
            
            # Vendas após o último período de compra
            sales_after = prod.sales_after_period(ReportController.repo.session, last_purchase)
            
            # Média de vendas diárias após o último período de compra
            avg_sales_daily = sales_after / days_since_last_purchase
            
            # Estoque de segurança (Security Stock) calculado com base no desvio padrão
            desvio_padrao = prod.daily_demand_variance(ReportController.repo.session, last_purchase) or 0
            security_stock = 1.65 * desvio_padrao
            
            # Média de vendas diárias multiplicada pelo número de dias de estoque desejado (60 dias)
            avg_sales = avg_sales_daily * 60
            
            # Calculando a quantidade a ser comprada para manter o estoque por 60 dias
            quantidade_comprar = avg_sales + security_stock
            
            dias_suprimento = stock / avg_sales_daily
            
            quantidade_comprar -= stock
            if quantidade_comprar < 0: quantidade_comprar
            # Montando o resultado para cada produto
            result = {
                'cdprincipal': prod.cdprincipal,
                'dsdetalhe': prod.dsdetalhe,
                'stock': stock,
                'dias_suprimento': dias_suprimento,
                'sugestao': quantidade_comprar,
                'dtreferencia': last_purchase.strftime('%d/%m/%Y'),
                'sales': sales_after,
                'security_stock': security_stock,
                'avg_sales_daily': avg_sales_daily,
                'avg_sales_60_days': avg_sales
            }
            
            
            retorno.append(result)
        return retorno
    
    @classmethod
    def get_router(cls):
        return cls.router