from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Docitem(Base):
    __tablename__ = 'docitem'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, primary_key=True)
    iddocumento = Column(String, ForeignKey('wshop.documen.iddocumento'))
    dtreferencia = Column(Date) 
    documento = relationship("Document", back_populates="docitems")