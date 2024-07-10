from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.model.base import Base


class ProductInfo(Base):
    __tablename__ = 'produto'
    __table_args__ = {'schema': 'wshop'}
    idproduto = Column(String, primary_key=True)
    idgrupo = Column(String, ForeignKey('wshop.grupo.idgrupo'))
    nmproduto = Column(String)
    group = relationship("Group", back_populates="products", primaryjoin="Group.idgrupo == ProductInfo.idgrupo")
    product = relationship("Product", back_populates="product_info", uselist=False, primaryjoin="ProductInfo.idproduto == Product.idproduto")

    def __repr__(self):
        return f"<Product_info(id={self.idproduto} ds={self.nmproduto})>"