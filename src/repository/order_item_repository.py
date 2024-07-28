from typing import Dict, List

from sqlalchemy.exc import IntegrityError
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
                [OrderItem(**order_item.model_dump())
                for order_item in order_items]
            )
            session.commit()
            return True

        except IntegrityError as e:
            
            if isinstance(e.params, list):
                item_name = e.params[0][3]
            elif isinstance(e.params, tuple):
                item_name = e.params[3]
            else:
                item_name = ''
            if session:
                session.rollback()
            
            raise HTTPException(
                400,
                f'O produto {item_name} ja esta em uma compra em aberto'
            ) from e

        except Exception as e:
            if session:
                session.rollback()
            raise HTTPException(
                500,
                'Ops, occoreu um erro'
            ) from e
        finally:
            if session:
                session.close()
