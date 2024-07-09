from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Familia(Base):
    __tablename__ = 'familia'
    __table_args__ = {'schema': 'wshop'}
    idfamilia = Column(String, primary_key=True)
    dsfamilia = Column(String)
    produtos = relationship("Produto", back_populates="familia", primaryjoin="Produto.idfamilia == Familia.idfamilia")
