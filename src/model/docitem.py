from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Docitem(Base):
    __tablename__ = 'docitem'
    __table_args__ = {'schema': 'wshop'}
    iddocumentoitem = Column(String, primary_key=True)
    iddetalhe = Column(String, ForeignKey('wshop.detalhe.iddetalhe'))
    iddocumento = Column(String, ForeignKey('wshop.documen.iddocumento'))
    dtreferencia = Column(Date) 
    documento = relationship("Document", back_populates="docitems")
    produtos = relationship("Produto", back_populates="docitems")
    
    def __repr__(self):
        return (
            f"<Docitem(id={self.iddocumento} "
            f"data={self.dtreferencia} idproduto={self.iddetalhe})>"
        )
