from pydantic import BaseModel
from typing import Any, Optional


class BaseResponseModel(BaseModel):
    data: Any
    message: Optional[str] = None


class BaseErrorModel(BaseModel):
    error: Optional[str] = None
