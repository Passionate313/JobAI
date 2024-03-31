from typing import Any, Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    data: Optional[Any]
    code: int
    message: str


class ErrorResponseModel(BaseModel):
    error: Optional[Any]
    code: int
    message: str
