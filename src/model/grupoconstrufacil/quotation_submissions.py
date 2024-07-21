#ext
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
#app
from src.model.grupoconstrufacil.base import Base

class QuotationSubmission(Base):
    __tablename__ = 'quotation_submissions'
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey('quotations.quotation_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    quotation_items = relationship("QuotationSubmissionItem", back_populates="submission")
    user = relationship("User", back_populates="quote_submitions")
