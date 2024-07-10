from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Produto(Base):
    __tablename__ = 'detalhe'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, primary_key=True)
    idproduto = Column(String, ForeignKey('wshop.produto.idproduto'))
    idfamilia = Column(String, ForeignKey('wshop.familia.idfamilia'))
    dsdetalhe = Column(String)
    stdetalheativo = Column(Boolean)
    familia = relationship("Familia", back_populates="produtos", primaryjoin="Produto.idfamilia == Familia.idfamilia")
    produto_info = relationship("ProdutoInfo", back_populates="produto", uselist=False, primaryjoin="Produto.idproduto == ProdutoInfo.idproduto")
    docitems = relationship("Docitem", back_populates="produtos")
    
    def __repr__(self):
        return f"<Produto(id={self.iddetalhe} ds={self.dsdetalhe})>"
