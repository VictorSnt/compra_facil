from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Grupo(Base):
    __tablename__ = 'grupo'
    __table_args__ = {'schema': 'wshop'}
    idgrupo = Column(String, primary_key=True)
    nmgrupo = Column(String)
    produtos = relationship("ProdutoInfo", back_populates="grupo", primaryjoin="ProdutoInfo.idgrupo == Grupo.idgrupo")

    def __repr__(self):
        return f"<Grupo(id={self.idgrupo} ds={self.nmgrupo})>"