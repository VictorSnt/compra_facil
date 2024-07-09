from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import  HTTPException, status

class NotFoundException(HTTPException):

    def __init__(self, headers: Dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, 'Nenhum registro', headers)
