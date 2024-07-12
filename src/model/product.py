#std
from datetime import datetime, timedelta, date
import statistics
#ext
from sqlalchemy import Boolean, Column, ForeignKey, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
#app
from src.model.document import Document
from src.model.docitem import Docitem
from src.model.stock import Stock
from src.model.base import Base


class Product(Base):
    __tablename__ = 'detalhe'
    __table_args__ = {'schema': 'wshop'}
    iddetalhe = Column(String, ForeignKey('wshop.estoque.iddetalhe'), primary_key=True)
    idproduto = Column(String, ForeignKey('wshop.produto.idproduto'))
    idfamilia = Column(String, ForeignKey('wshop.familia.idfamilia'))
    dsdetalhe = Column(String)
    cdprincipal = Column(String)
    stdetalheativo = Column(Boolean)
    family = relationship(
        "Family", 
        back_populates="products",
        primaryjoin="Product.idfamilia == Family.idfamilia"
    )
    product_info = relationship(
        "ProductInfo", 
        back_populates="product",
        uselist=False,
        primaryjoin="Product.idproduto == ProductInfo.idproduto"
    )
    docitems = relationship("Docitem", back_populates="products")
    stocks = relationship("Stock", back_populates="product")
    latest_stock = relationship(
        "Stock",
        primaryjoin="and_(Product.iddetalhe == Stock.iddetalhe,"
        "Stock.dtreferencia == (select(func.max(Stock.dtreferencia))"
        ".where(Stock.iddetalhe == Product.iddetalhe)))",
        uselist=False,
        overlaps="stocks,product"
    )

    def last_relevant_purchase(self, session: Session) -> datetime:
        result = (
            session.query(Document.dtreferencia)
            .join(Docitem)
            .filter(
                Docitem.iddetalhe == self.iddetalhe,
                Document.tpoperacao == 'C',
                Document.dtreferencia <= (date.today() - timedelta(days=25))
            )
            .order_by(
                Document.dtreferencia.desc()
            )
            .limit(1)
        ).scalar()

        if not result: raise ValueError(
            f'result shoud be datetime, got {result} instead'
        )

        return result

    def sales_after_period(self, session: Session, period: datetime) -> float:

        if not isinstance(period, datetime):
            raise ValueError("The period must be a datetime instance")

        result = session.query(func.sum(Stock.qtvenda)).join(Product).filter(
        Product.iddetalhe == self.iddetalhe,
        Stock.dtreferencia > period,
        Stock.qtvenda > 0
        ).scalar()

        return result if result is not None else 0.0

    def daily_demand_variance(
        self,
        session: Session,
        initial_period: datetime
    ) -> float:

        if not isinstance(initial_period, datetime):
            raise ValueError("The initial period must be a datetime instance")

        result = session.query((Stock.qtvenda)).join(Product).filter(
        Product.iddetalhe == self.iddetalhe,
        Stock.dtreferencia >= initial_period,
        ).all()

        if not result:
            raise ValueError("result is none, this product does not have sales")

        daily_demand = [qtvenda or 0 for (qtvenda,) in result ]
        min_data_to_calc = 2

        if len(daily_demand) < min_data_to_calc:
            raise ValueError("Not enough data to calculate variance")
        demand_variance = statistics.stdev(daily_demand)
        return demand_variance

    def __repr__(self):
        return f"<Product(id={self.iddetalhe} ds={self.dsdetalhe})>"
