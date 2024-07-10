from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Family(Base):
    __tablename__ = 'familia'
    __table_args__ = {'schema': 'wshop'}
    idfamilia = Column(String, primary_key=True)
    dsfamilia = Column(String)
    products = relationship("Product", back_populates="family", primaryjoin="Product.idfamilia == Family.idfamilia")
 
    def __repr__(self):
        return f"<Family(id={self.idfamilia} ds={self.dsfamilia})>"