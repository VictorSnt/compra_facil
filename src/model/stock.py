from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Stock(Base):
    __tablename__ = 'estoque'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, primary_key=True)
    dtreferencia = Column(Date)
    qtcompra = Column(Float)
    qtvenda = Column(Float)
    qtestoque = Column(Float)
    product = relationship("Product", back_populates="stocks", primaryjoin="Stock.iddetalhe == Product.iddetalhe")
    
    def __repr__(self):
        return f"<Stock(produto={self.iddetalhe} ds={self.iddetalhe} data={self.dtreferencia})>"
