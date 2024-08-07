from typing import List
from src.model.grupoconstrufacil.models import QuotationSubmission
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException
from src.model.product import Product
from src.model.stock import Stock
from src.schemas.quotation_schema import GetQuotationSubmit, GetQuotationSubmitItem


class QuotSubimitRepository:

    def find_by_id(self, quotation_id) -> List[GetQuotationSubmit]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            adt_session = SessionMaker.alterdata_session()
            quotes: List[QuotationSubmission] | None = (
                session.query(QuotationSubmission)
                .filter(QuotationSubmission.quotation_id == quotation_id)
            ).all()
            if not quotes: raise NotFoundException

            return (
                [
                    GetQuotationSubmit(
                    quotation_id=quote.quotation_id,
                    submission_id=quote.submission_id,
                    user_id=quote.user_id,
                    user_name=quote.user.name,
                    items=[
                        GetQuotationSubmitItem(
                            qtitem=item.qtitem,
                            submission_item_id=item.submission_item_id,
                            submission_id=item.submission_id,
                            item_brand=item.item_brand,
                            item_brand2=item.item_brand2,
                            item_name=item.item_name,
                            item_price=item.item_price,
                            vllastcompra = round(
                                (adt_session.query(Stock.vlcompra / Stock.qtcompra)
                                .join(Product)
                                .filter(Product.dsdetalhe == item.item_name)
                                .filter(Stock.qtcompra > 0)
                                .filter(Stock.vlcompra > 1)
                                .order_by(Stock.dtreferencia.desc())
                                .limit(1)
                                .scalar()) or 0, 2
                            ),
                            item_price2=item.item_price2,
                        )for item in quote.quotation_items if item
                    ])for quote in quotes
                ]
            )
        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise NotFoundException from e
        finally:
            if session:
                session.close()
            if adt_session:
                adt_session.close()
