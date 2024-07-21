#ext
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey('quotation.quotation_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", back_populates="quote_submitions")
