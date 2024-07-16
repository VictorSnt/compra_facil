from datetime import date
from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import relationship
from src.model.grupoconstrufacil.base import Base

class Quotation(Base):
    __tablename__ = 'quotations'
    quotation_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(70))
    created_at = Column(Date, default=date.today())
    status = Column(Boolean, nullable=False, default=True)
    items = relationship("QuotationItem", back_populates="quotation")

    def __repr__(self):
        return (
            f"<Quotation(id={self.quotation_id} "
            f"status={self.status})>"
        )
