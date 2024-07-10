from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Pessoa(Base):
    __tablename__ = 'pessoas'
    __table_args__ = {'schema': 'wshop'}
    idpessoa = Column(String, primary_key=True)
    nmpessoa = Column(String)
    sttipopessoa = Column(String)
    documentos = relationship(
        "Document", back_populates="pessoa", 
        primaryjoin="Pessoa.idpessoa == Document.idpessoa"
    )
    
    def __repr__(self):
        return f"<Pessoa(id={self.idpessoa} ds={self.nmpessoa})>"
    