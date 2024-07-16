from typing import List

from fastapi import HTTPException
from src.model.grupoconstrufacil.models import Quotation
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException
from src.schemas.quotation_schema import GetQuotation, GetQuotationItem


class QuotationRepository:

    def find_all(self) -> List[Quotation]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = session.query(Quotation).all()
            for quote in result:
                GetQuotation(
                    quotation_id=quote.quotation_id,
                    description=quote.description,
                    created_at=quote.created_at,
                    status=quote.status,
                    items=[
                        GetQuotationItem(
                        cdprincipal=item.cdprincipal,
                        dsdetalhe=item.dsdetalhe,
                        iddetalhe=item.iddetalhe,
                        qtitem=item.qtitem,
                        quotation_id=item.quotation_id,
                        quotation_item_id=item.quotation_item_id) 
                        for item in quote.items if item]
                )
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

    def create(self) -> str:
        session = None
        try:
            session = SessionMaker.own_db_session()
            new_quotation = Quotation()
            new_quotation.description = 'Teste' 
            session.add(new_quotation)
            session.commit()
            return new_quotation.quotation_id
        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise HTTPException(400, 'Falha ao criar cotação') from e
        finally:
            if session:
                session.close()
