from pydantic import BaseModel
from datetime import datetime


class CookingHistoryResponse(BaseModel):
    userId: int
    recipeId: int
    recipeName: str
    recipeDescription: str | None = None
    likesCount: int | None = 0
    createdAt: datetime

    class Config:
        from_attributes = True


class CookingHistoryRequest(BaseModel):
    recipe_id: int
