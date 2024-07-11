from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Product(Base):
    __tablename__ = 'detalhe'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, ForeignKey('wshop.estoque.iddetalhe'), primary_key=True)
    idproduto = Column(String, ForeignKey('wshop.produto.idproduto'))
    idfamilia = Column(String, ForeignKey('wshop.familia.idfamilia'))
    dsdetalhe = Column(String)
    stdetalheativo = Column(Boolean)
    family = relationship("Family", back_populates="products", primaryjoin="Product.idfamilia == Family.idfamilia")
    product_info = relationship("ProductInfo", back_populates="product", uselist=False, primaryjoin="Product.idproduto == ProductInfo.idproduto")
    docitems = relationship("Docitem", back_populates="products")
    stocks = relationship("Stock", back_populates="product")
    latest_stock = relationship("Stock",
        primaryjoin="and_(Product.iddetalhe == Stock.iddetalhe, Stock.dtreferencia == (select(func.max(Stock.dtreferencia)).where(Stock.iddetalhe == Product.iddetalhe)))",
        uselist=False
    )
    
    def __repr__(self):
        return f"<Product(id={self.iddetalhe} ds={self.dsdetalhe})>"
