#ext
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base

class QuotationSubmission(Base):
    __tablename__ = 'quotation_submissions'
    quotation_submission_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, nullable=False)
    supplier_name = Column(String)
    quotation_id = Column(Integer, ForeignKey('quotations.quotation_id'), nullable=False)
    quotation_items = relationship("QuotationSubmissionItem", back_populates="submission")
