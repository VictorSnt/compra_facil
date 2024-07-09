from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Produto(Base):
    __tablename__ = 'detalhe'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, primary_key=True)
    idproduto = Column(String, ForeignKey('wshop.produto.idproduto'))
    idfamilia = Column(String, ForeignKey('wshop.familia.idfamilia'))
    dsdetalhe = Column(String)
    familia = relationship("Familia", back_populates="produtos", primaryjoin="Produto.idfamilia == Familia.idfamilia")
    produto_info = relationship("ProdutoInfo", back_populates="produto", uselist=False, primaryjoin="Produto.idproduto == ProdutoInfo.idproduto")
