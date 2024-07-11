from datetime import datetime
from fastapi import APIRouter, Query

from src.exceptions.err import NotFoundException
from src.repository.product_repository import ProductRepository
from src.model.models import *

router = APIRouter(prefix="/report")
Product
class ReportService:
    
    def __init__(self, repository: ProductRepository) -> None:
        self.repo = repository
        
    @router.get('/shopping_sugestion')
    def shopping_sugestion(
        self,
        product_ids = Query()
    ):
        retorno = []
        prods = self.repo.find_products_with_current_stock(product_ids)
        for prod in prods:
            last_purchase  = prod.last_relevant_purchase(self.repo.session)
            days_sinse_last_purchase = (datetime.now() - last_purchase).days
            sales_after  = prod.sales_after_period(self.repo.session, last_purchase)
            avg_sales = sales_after / days_sinse_last_purchase
            result = {
                'cdprincipal': prod.cdprincipal, 'dsdetalhe': prod.dsdetalhe,
                'stock': prod.latest_stock, 'sugestion': avg_sales * 60, 
                'dtreferencia': last_purchase.strftime('%d/%m/%Y'),
                'sales': sales_after
            }
            retorno.append(result)
            
   
        return retorno