#str
from typing import List
#ext
from fastapi import APIRouter, Query, Depends, Path
#app
from src.database.redis_cache_maker import RedisConnection
from src.factory.product_service_factory import ProductServiceFactory
from src.schemas.product_schema import GetProduct, GetProductWithStock
from src.services.produto_service import ProductService


class ProductController:

    router = APIRouter(prefix='/products')

    @staticmethod
    @router.get('/', response_model=List[GetProduct])
    def get_produtos(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_service
        ),
        only_active: bool = Query(True),
        family_ids: List[str] = Query(None),
        group_ids: List[str] = Query(None),
        supplier_ids: List[str] = Query(None)
        ):

        return service.find_all(only_active, family_ids, group_ids, supplier_ids)


    @staticmethod
    @router.delete('/{product_id}')
    def inativate_product(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_service
        ),
        product_id: str = Path()
    ):
        redis_key = f'suggestion:{product_id}'
        # with RedisConnection() as redis:
        #     redis.delete(redis_key)
        return service.inativate_product(product_id)

    @classmethod
    def get_router(cls):
        return cls.router
