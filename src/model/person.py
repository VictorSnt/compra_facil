from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Person(Base):
    __tablename__ = 'pessoas'
    __table_args__ = {'schema': 'wshop'}
    idpessoa = Column(String, primary_key=True)
    nmpessoa = Column(String)
    sttipopessoa = Column(String)
    documentos = relationship(
        "Document", back_populates="person", 
        primaryjoin="Person.idpessoa == Document.idpessoa"
    )
    
    def __repr__(self):
        return f"<Person(id={self.idpessoa} ds={self.nmpessoa})>"
    