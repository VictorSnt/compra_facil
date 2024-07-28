from typing import List

from fastapi import HTTPException
from src.model.grupoconstrufacil.models import Order
from src.database.db_session_maker import SessionMaker
from src.exceptions.err import NotFoundException
from src.model.grupoconstrufacil.user import User
from src.model.order_item import OrderItem
from src.schemas.order_schema import CreateOrder
from src.schemas.order_schema import GetOrder, GetOrderItens


class OrdersRepository:

    def find_all(self) -> List[Order]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = (
                session.query(Order)
                .filter(Order.status == True)
                .all()
            )

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

    def find_by_user(self, user_id: str) -> List[GetOrder]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result: Order|None = (
                session.query(Order)
                .filter(Order.user_id == user_id)
                .filter(Order.status == True)
            ).scalar()

            if not result:
                raise NotFoundException

            return result.order_id

        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise NotFoundException from e
        finally:
            if session:
                session.close()

    def find_by_id(self, order_id) -> List[GetOrder]:
        session = None
        try:
            session = SessionMaker.own_db_session()
            result = (
                session.query(Order)
                .filter(Order.order_id == order_id)
                .filter(Order.status == True)
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

    def create(self, order_dto: CreateOrder) -> str:
        session = None
        try:
            session = SessionMaker.own_db_session()
            new_order = Order(**order_dto.model_dump())
            session.add(new_order)
            session.commit()
            session.refresh(new_order)
            return new_order.order_id
        except Exception as e:
            print(e)
            if session:
                session.rollback()
            raise HTTPException(400, 'Falha ao criar cotação') from e
        finally:
            if session:
                session.close()

    def finish_order(self, order_id) -> str:
        session = None
        try:
            session = SessionMaker.own_db_session()
            order: Order| None  = (
                session.query(Order)
                .filter(Order.order_id == order_id)
                .filter(Order.status == True)
            ).scalar()
            if order:
                order.status = False
                session.add(order)
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

    def __format_response(self, data: List[Order]):
        response = []
        for order in data:
            user: User = order.user
            items: List[OrderItem] = order.items
            response.append(GetOrder(
                order_id=order.order_id,
                user_id=user.id,
                user_name=user.name,
                items=[
                    GetOrderItens(
                    quotation_item_id=item.quotation_item_id,
                    order_item_id=item.order_item_id,
                    dsdetalhe=item.dsdetalhe,
                    iddetalhe=item.dsdetalhe,
                    order_id=item.order_id,
                    qtcompra=item.qtcompra,
                    vlcompra=item.vlcompra,
                    ) for item in items if item
                ]
            ))
        return response
