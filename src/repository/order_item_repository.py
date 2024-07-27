from typing import Dict, List

from fastapi import HTTPException
from src.model.grupoconstrufacil.models import *
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException
from src.schemas.order_schema import CreateOrderItems


class OrderItemRepository:

    def find_all(self) -> List[OrderItem]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = session.query(OrderItem).all()
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
        order_items: List[CreateOrderItems]
    ) -> bool:
        session = None
        try:
            session = SessionMaker.own_db_session()
            session.bulk_save_objects(
                [ OrderItem(**order_item)
                for order_item in order_items]
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
