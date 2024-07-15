from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.orm import relationship
from src.model.grupoconstrufacil.base import Base

class Quotation(Base):
    __tablename__ = 'quotations'
    quotation_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Boolean, nullable=False, default=True)
    items = relationship("QuotationItem", back_populates="quotation")

    def __repr__(self):
        return (
            f"<Quotation(id={self.quotation_id} "
            f"status={self.status})>"
        )
