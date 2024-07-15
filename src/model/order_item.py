from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class OrderItem(Base):
    __tablename__ = 'peditem'
    __table_args__ = {'schema': 'wshop'}
    idpedido = Column(String, ForeignKey('wshop.pedidos.idpedido'), primary_key=True)
    iddetalhe = Column(String, ForeignKey('wshop.detalhe.iddetalhe'))
    qtpedida = Column(Float)

    def __repr__(self):
        return f"<Order(produto={self.idpedido} ds={self.qtpedida})>"
