from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base

class Document(Base):
    __tablename__ = 'documen'
    __table_args__ = {'schema': 'wshop'}
    iddocumento = Column(String, primary_key=True)
    dtreferencia = Column(Date)
    dtemissao = Column(Date)
    idpessoa = Column(String, ForeignKey('wshop.pessoas.idpessoa'))
    tpoperacao = Column(String)
    pessoa = relationship("Pessoa", back_populates="documentos")
    docitems = relationship("Docitem", back_populates="documento")