from typing import List

from fastapi import HTTPException
from src.model.grupoconstrufacil.models import Quotation
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException


class QuotationRepository:

    def find_all(self) -> List[Quotation]:
        session = None
        try:
            session = SessionMaker.own_db_session()
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

    def create(self) -> str:
        session = None
        try:
            session = SessionMaker.own_db_session()
            new_quotation = Quotation()
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
