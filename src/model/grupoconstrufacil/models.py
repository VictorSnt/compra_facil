from sqlalchemy import create_engine

from src.model.grupoconstrufacil.quotation import Quotation
from src.model.grupoconstrufacil.quotation_item import QuotationItem
from src.model.grupoconstrufacil.quotation_submission_items import QuotationSubmissionItem
from src.model.grupoconstrufacil.quotation_submissions import QuotationSubmission

from src.model.grupoconstrufacil.base import Base
engine2 = create_engine('sqlite:///database2.db')
Base.metadata.create_all(engine2)
