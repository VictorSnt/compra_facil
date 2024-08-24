from re import S
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from src.model.product import Product
from src.model.product_info import ProductInfo
from src.model.docitem import Docitem
from src.model.document import Document


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
        grupo_filter: Optional[List[str]] = None,
        supplier_ids: Optional[List[str]] = None
    ) -> List[Product]:

        query: Query = self.session.query(self.model)
        conditions = []
        result = []
        query = query.filter(self.model.stdetalheativo == True)

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
        
        if supplier_ids:
            supp_result = self.find_products_by_suppliers(supplier_ids)

            if conditions:
                result = supp_result + query.all()
            else:
                result = supp_result
        else: 
            result = query.all()

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
            .filter(self.model.stdetalheativo == True)
            .all()
        )

        self.session.close()
        return query

    def find_active_products(self) -> List[Product]:
        return (
            self.session.query(Product)
            .filter(Product.stdetalheativo == True)
            .all()
        )

    def find_similar_products(self, description: str, idfamilia: str)-> List[Product]:
        return (
            self.session.query(self.model)
            .filter(
                self.model.dsdetalhe.like(f'{description}%'),
                self.model.idfamilia == idfamilia
            ).all()
        )

    def find_by_id(
            self, product_id: str
        ) -> Product:

        result: Product = (
            self.session.query(self.model)
            .filter(self.model.iddetalhe == product_id)
            .filter(self.model.stdetalheativo == True)
            .scalar()
        )

        return result
