from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Order(Base):
    __tablename__ = 'pedidos'
    __table_args__ = {'schema': 'wshop'}
    idpedido = Column(String, primary_key=True)
    cdstatus = Column(String)

    def __repr__(self):
        return f"<Order(produto={self.idpedido} ds={self.cdstatus})>"
