from datetime import timedelta, date
from sqlalchemy import Boolean, Column, ForeignKey, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from src.model.base import Base
from src.model.docitem import Docitem
from src.model.document import Document
from src.model.stock import Stock
import statistics


class Product(Base):
    __tablename__ = 'detalhe'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, ForeignKey('wshop.estoque.iddetalhe'), primary_key=True)
    idproduto = Column(String, ForeignKey('wshop.produto.idproduto'))
    idfamilia = Column(String, ForeignKey('wshop.familia.idfamilia'))
    dsdetalhe = Column(String)
    cdprincipal = Column(String)
    stdetalheativo = Column(Boolean)
    family = relationship("Family", back_populates="products", primaryjoin="Product.idfamilia == Family.idfamilia")
    product_info = relationship("ProductInfo", back_populates="product", uselist=False, primaryjoin="Product.idproduto == ProductInfo.idproduto")
    docitems = relationship("Docitem", back_populates="products")
    stocks = relationship("Stock", back_populates="product")
    latest_stock = relationship("Stock",
        primaryjoin="and_(Product.iddetalhe == Stock.iddetalhe, Stock.dtreferencia == (select(func.max(Stock.dtreferencia)).where(Stock.iddetalhe == Product.iddetalhe)))",
        uselist=False
    )
    
    def last_relevant_purchase(self, session: Session) -> date:
        result = session.query(Document.dtreferencia).join(Docitem).filter(
            Docitem.iddetalhe == self.iddetalhe,
            Document.tpoperacao == 'C',
            Document.dtreferencia <= (date.today() - timedelta(days=25))
            
        ).order_by(Document.dtreferencia.desc()).limit(1).scalar()
        return result if result else None
    
    def sales_after_period(self, session: Session, period):
        if period:
            result = session.query(func.sum(Stock.qtvenda)).join(Product).filter(
            Product.iddetalhe == self.iddetalhe,
            Stock.dtreferencia > period,
            Stock.qtvenda > 0
            ).scalar()
            
            return result if result is not None else 0.0
    
    def daily_demand_variance(self, session: Session, initial_period):
        if not initial_period:
            return
        result = session.query((Stock.qtvenda)).join(Product).filter(
        Product.iddetalhe == self.iddetalhe,
        Stock.dtreferencia >= initial_period,
        ).all()
        if not result:
            return
        daily_demand = [qtvenda for (qtvenda,) in result]
        input(daily_demand)
        media = statistics.mean(daily_demand)
        print(f"Média da demanda diária (incluindo zeros): {media}")

        # Calculando o desvio padrão
        desvio_padrao = statistics.stdev(daily_demand)
        print(f"Desvio padrão da demanda diária (incluindo zeros): {desvio_padrao}")
        return desvio_padrao
    
    def __repr__(self):
        return f"<Product(id={self.iddetalhe} ds={self.dsdetalhe})>"
