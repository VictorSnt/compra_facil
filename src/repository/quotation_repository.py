from typing import List

from fastapi import HTTPException
from src.model.grupoconstrufacil.models import Quotation
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException
from src.model.grupoconstrufacil.quotation_item import QuotationItem
from src.schemas.quotation_schema import GetQuotation, GetQuotationItem


class QuotationRepository:

    def find_all(self) -> List[Quotation]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = session.query(Quotation).all()
            if not result:
                raise NotFoundException

            return self.__format_response(result)

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise NotFoundException from e
        finally:
            if session:
                session.close()

    def find_by_id(self, quotation_id) -> List[GetQuotation]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = (
                session.query(Quotation)
                .filter(Quotation.quotation_id == quotation_id) 
            ).all()

            if not result:
                raise NotFoundException

            return self.__format_response(result)

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise NotFoundException from e
        finally:
            if session:
                session.close()

    def create(self, title: str) -> str:
        session = None
        try:
            session = SessionMaker.own_db_session()
            new_quotation = Quotation()
            new_quotation.description = title 
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

    def delete(self, quotation_id) -> str:
        session = None
        try:
            session = SessionMaker.own_db_session()
            q: Quotation| None  = (
                session.query(Quotation)
                .filter(Quotation.quotation_id == quotation_id)
            ).scalar()
            if q:
                q.status = False
                session.add(q)
                session.commit()
                return

            raise NotFoundException

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise HTTPException(400, 'Falha ao inativar cotação') from e
        finally:
            if session:
                session.close()

    def filter_not_quoted_items(
        self, iddetalhe_list: List[str]
    ) -> List[str]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            iddetalhe_in_quote: List[str] = (
                session.query(QuotationItem.iddetalhe)
                .join(Quotation)
                .filter(Quotation.status == True)
            ).all()
            formated_ids = [item[0] for item in iddetalhe_in_quote]
            result = [
                iddetalhe for iddetalhe in iddetalhe_list 
                if iddetalhe not in formated_ids
            ]
           
            return result

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise NotFoundException from e
        finally:
            if session:
                session.close()
    
    
    def __format_response(self, data):
        response = []
        for quote in data:
            response.append(GetQuotation(
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
            ))
        return response
