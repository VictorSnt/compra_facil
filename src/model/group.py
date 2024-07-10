from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class Group(Base):
    __tablename__ = 'grupo'
    __table_args__ = {'schema': 'wshop'}
    idgrupo = Column(String, primary_key=True)
    nmgrupo = Column(String)
    products = relationship("ProductInfo", back_populates="group", primaryjoin="ProductInfo.idgrupo == Group.idgrupo")

    def __repr__(self):
        return f"<Group(id={self.idgrupo} ds={self.nmgrupo})>"