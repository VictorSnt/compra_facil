from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class ProdutoInfo(Base):
    __tablename__ = 'produto'
    __table_args__ = {'schema': 'wshop'}
    idproduto = Column(String, primary_key=True)
    idgrupo = Column(String, ForeignKey('wshop.grupo.idgrupo'))
    nmproduto = Column(String)
    grupo = relationship("Grupo", back_populates="produtos", primaryjoin="Grupo.idgrupo == ProdutoInfo.idgrupo")
    produto = relationship("Produto", back_populates="produto_info", uselist=False, primaryjoin="ProdutoInfo.idproduto == Produto.idproduto")

    def __repr__(self):
        return f"<Produto_info(id={self.idproduto} ds={self.nmproduto})>"