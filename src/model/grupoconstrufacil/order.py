#ext
from sqlalchemy import Boolean, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Boolean, default=True)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
