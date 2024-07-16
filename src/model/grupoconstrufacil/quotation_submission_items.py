#ext
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base

class QuotationSubmissionItem(Base):
    __tablename__ = 'quotation_submission_items'
    quotation_submission_item_id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(
        Integer, ForeignKey('quotation_submissions.quotation_submission_id'), nullable=False
    )
    item_name = Column(String(80), nullable=False)
    item_brand = Column(String(80), nullable=False)
    item_price = Column(Float, nullable=False)
    item_brand2 = Column(String(80), nullable=True)
    item_price2 = Column(Float, nullable=True)
    submission = relationship(
        "QuotationSubmission", 
        back_populates="quotation_items"
    )
