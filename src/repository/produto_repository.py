from re import S
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from src.model.produto import Produto
from src.model.produto_info import ProdutoInfo
from src.model.docitem import Docitem
from src.model.document import Document
from src.model.produto import Produto


class ProdutoRepository:
    
    def __init__(
        self, session: Session, model: Produto, 
        model_2: ProdutoInfo    
    ) -> None:
        
        self.session: Session = session
        self.model: Produto = model
        self.model_2: ProdutoInfo = model_2
    
    def find_all(
        self,
        active_only: bool,
        familia_filter: Optional[List[str]] = None,
        grupo_filter: Optional[List[str]] = None 
    ) -> List[Produto]:
        
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
        
        result: List[Produto] = query.all()
        
        self.session.close()
        
        return result

    def find_products_by_suppliers(
        self, fornecedor_ids: List[str]
        ) -> List[Produto]:
        
        query = (
            self.session.query(self.model)
            .join(Docitem, Docitem.iddetalhe == Produto.iddetalhe)
            .join(Document, Docitem.iddocumento == Document.iddocumento)
            .filter(Document.idpessoa.in_(fornecedor_ids))
            .all()
        )
        
        self.session.close()
        return query 