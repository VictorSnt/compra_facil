from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from src.model.grupoconstrufacil.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    cnpj = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    quote_submitions = relationship('QuotationSubmission', back_populates="user")
