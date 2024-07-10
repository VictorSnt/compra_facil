from typing import List
from fastapi import APIRouter, Query
from fastapi.params import Depends

from src.factory.pessoa_service_factory import PessoaServiceFactory
from src.schemas.pessoa_schema import GetPessoa
from src.schemas.produto_schema import GetProduto
from src.services.pessoa_service import PessoaService



class PessoaController:
    
    router = APIRouter(prefix='/pessoas')
    
    @router.get('/', response_model=List[GetPessoa])
    def get_pessoas(
        service: PessoaService = Depends(
            PessoaServiceFactory.build_default_Service
        ),
        only_suppliers: bool = Query(False) 
        ):
        
        if only_suppliers:
            return service.find_all_suppliers()
        return service.find_all()
          
    @classmethod
    def get_router(cls):
        return cls.router
