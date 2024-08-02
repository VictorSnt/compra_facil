#ext
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base


class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    quotation_item_id = Column(
        Integer,
        ForeignKey('quotation_items.quotation_item_id'),
        nullable=False,
        unique=True
    )
    iddetalhe = Column(String(50), nullable=False)
    dsdetalhe = Column(String(50), nullable=False)
    qtcompra = Column(Float, nullable=False)
    vlcompra = Column(Float, nullable=False)
    vllastcompra = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    