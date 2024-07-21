#ext
from tokenize import String
from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base

class Order(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    quotation_id = Column(Integer, ForeignKey('quotation.quotation_id'), nullable=False)
    iddetalhe = Column(String(50), nullable=False)
    dsdetalhe = Column(String(50), nullable=False)
    qtcompra = Column(Float, nullable=False)
