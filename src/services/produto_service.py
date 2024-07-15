from typing import List
from fastapi import APIRouter, HTTPException

from src.exceptions.err import NotFoundException
from src.repository.product_repository import ProductRepository
from src.schemas.product_schema import GetProduct, GetProductWithStock

router = APIRouter()


class ProductService:

    def __init__(self, repository: ProductRepository) -> None:
        self.repo = repository

    def find_all(
        self, only_active: bool,
        familia_filter: List[str]|None,
        grupo_filter: List[str]|None,
        supplier_ids: List[str]|None
    ):
        response = self.repo.find_all(
            only_active, familia_filter, grupo_filter, supplier_ids
        )

        if not response:
            raise NotFoundException
        print('serc')
        return [
            GetProduct(
                iddetalhe=product.iddetalhe,
                dsdetalhe=product.dsdetalhe,
            ) for product in response
        ]

    def find_all_suppliers_products(self, fornecedor_ids):

        response = self.repo.find_products_by_suppliers(fornecedor_ids)

        if not response:
            raise NotFoundException

        return [
            GetProduct(
                iddetalhe=product.iddetalhe, 
                dsdetalhe=product.dsdetalhe
            )for product in response
        ]


    def inativate_product(self, product_id):
        product = self.repo.find_by_id(product_id)
        if not product:
            raise NotFoundException
        product.stdetalheativo = False
        try:
            # self.repo.session.add(product)
            # self.repo.session.commit()
            return {f'Produto {product} inativado'}
        except Exception as e:
            print(e)
            self.repo.session.rollback()
            return HTTPException(
                400, f'ouve uma falha o inativar o: {product}'
            )
