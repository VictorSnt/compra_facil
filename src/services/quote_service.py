
from typing import List

from fastapi import HTTPException
#app
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema
from src.model.grupoconstrufacil.models import QuotationItem, Quotation
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException


class QuoteService:

    def create_quotation(self, products: List[PurchaseSuggestionSchema]):
        try:
            session = SessionMaker.create_session(quotes_db=True)
            new_quotation = Quotation()
            session.add(new_quotation)
            session.commit()
            quotation_items = []
            for product in products:
                quotation_item = {
                    'quotation_id': new_quotation.quotation_id,
                    'iddetalhe': product.iddetalhe,
                    'cdprincipal': product.cdprincipal,
                    'dsdetalhe': product.dsdetalhe,
                    'qtitem': product.sugestao,
                }
                quotation_items.append(quotation_item)

            session.bulk_save_objects(
                [ QuotationItem(**quotation_item) 
                for quotation_item in quotation_items]
            )
            session.commit()

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise HTTPException(404, 'Falha ao criar cotação') from e
        finally:
            if session:
                session.close()

    def find_all(self):
        try:
            session = SessionMaker.create_session(quotes_db=True)
            result = session.query(Quotation).all()
            if not result:
                raise NotFoundException
            return result

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise NotFoundException from e
        finally:
            if session:
                session.close()
