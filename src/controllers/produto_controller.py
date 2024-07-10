from typing import List
from fastapi import APIRouter
from fastapi.params import Depends, Query

from src.factory.produto_service_factory import ProdutoServiceFactory
from src.schemas.produto_schema import GetProduto
from src.services.produto_service import ProdutoService



class ProdutoController:
    
    router = APIRouter(prefix='/produto')
    
    @router.get('/', response_model=List[GetProduto])
    def get_produtos(
        service: ProdutoService = Depends(
            ProdutoServiceFactory.build_default_Service
        ),
        only_active: bool = Query(True),
        familia_filter: List[str] = Query(None),
        grupo_filter: List[str] = Query(None)
        ):
        
        return service.find_all(only_active, familia_filter, grupo_filter)
    
    @router.get('/fornecedores', response_model=List[GetProduto])
    def get_produtos_fornecedor(
        service: ProdutoService = Depends(
            ProdutoServiceFactory.build_default_Service
        ),
        fornecedor_ids: List[str] = Query() 
        ):
        
        return service.find_all_suppliers_products(fornecedor_ids)
    
    @classmethod
    def get_router(cls):
        return cls.router
