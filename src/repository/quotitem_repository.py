from typing import Dict, List

from fastapi import HTTPException
from src.model.grupoconstrufacil.models import *
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException
from src.schemas.purchase_suggestion_schema import PurchaseSuggestionSchema


class QuotItemRepository:

    def find_all(self) -> List[QuotationItem]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = session.query(QuotationItem).all()
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

    def bulk_create(
        self,
        quotation_id: str,
        products: List[PurchaseSuggestionSchema]
    ) -> bool:
        session = None
        try:
            session = SessionMaker.own_db_session()
            quot_items_dict = self._format_suggest_to_quotation(
                quotation_id, products
            )
            session.bulk_save_objects(
                [ QuotationItem(**quotation_item) 
                for quotation_item in quot_items_dict]
            )
            session.commit()
            return True

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise HTTPException(400, 'Falha ao criar itens da cotação') from e
        finally:
            if session:
                session.close()

    def _format_suggest_to_quotation(
        self,
        quotation_id: str,
        products: List[PurchaseSuggestionSchema],
    ) -> List[Dict]:
        quotation_items = []
        for product in products:
            quotation_item = {
                'quotation_id': quotation_id,
                'iddetalhe': product.iddetalhe,
                'cdprincipal': product.cdprincipal,
                'dsdetalhe': product.dsdetalhe,
                'qtitem': product.sugestao,
            }
            quotation_items.append(quotation_item)
        return quotation_items
