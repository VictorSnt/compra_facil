from re import S
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from src.model.product import Product
from src.model.product_info import ProductInfo
from src.model.docitem import Docitem
from src.model.document import Document
from src.model.product import Product


class ProductRepository:
    
    def __init__(
        self, session: Session, model: Product, 
        model_2: ProductInfo    
    ) -> None:
        
        self.session: Session = session
        self.model: Product = model
        self.model_2: ProductInfo = model_2
    
    def find_all(
        self,
        active_only: bool,
        familia_filter: Optional[List[str]] = None,
        grupo_filter: Optional[List[str]] = None 
    ) -> List[Product]:
        
        query: Query = self.session.query(self.model)
        
        
        conditions = []

        if grupo_filter:
            query = query.join(
                self.model_2, 
                self.model_2.idproduto == self.model.idproduto
            )
            conditions.append(self.model_2.idgrupo.in_(grupo_filter))
        
        if familia_filter:
            conditions.append(self.model.idfamilia.in_(familia_filter))
        
        if conditions:
            query = query.filter(or_(*conditions))
        
        if active_only:
            query = query.filter(self.model.stdetalheativo == True)
        
        result: List[Product] = query.all()
        self.session.close()
        
        return result

    def find_products_by_suppliers(
        self, fornecedor_ids: List[str]
        ) -> List[Product]:
        
        query = (
            self.session.query(self.model)
            .join(Docitem, Docitem.iddetalhe == Product.iddetalhe)
            .join(Document, Docitem.iddocumento == Document.iddocumento)
            .filter(Document.idpessoa.in_(fornecedor_ids))
            .all()
        )
        
        self.session.close()
        return query 
    
    
    def find_products_with_current_stock(
        self, product_ids
        ) -> List[Product]:
        
        result: List[Product] = (
            self.session.query(self.model)
            .filter(self.model.iddetalhe.in_(product_ids))
            .all()
        )
        
        for product in result:
            input(product.latest_stock)
            # product.stock = sorted(product.stocks, key=lambda x: x.dtreferencia, reverse=True)
            
        