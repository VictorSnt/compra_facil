#ext
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base


class QuotationItem(Base):
    __tablename__ = 'quotation_items'
    quotation_item_id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey('quotations.quotation_id'), nullable=False)
    iddetalhe = Column(String(80), nullable=False)
    cdprincipal = Column(String(80), nullable=False)
    dsdetalhe = Column(String(80), nullable=False)
    qtitem = Column(Float)
    quotation = relationship("Quotation", back_populates="items")
