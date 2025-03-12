from pydantic import BaseModel
from typing import Optional
from .recipe_models import RecipeTypeEnum


class ForkedRecipeResponseModel(BaseModel):
    id: int
    userId: int
    recipeId: int
    recipeName: str
    description: Optional[str] = None
    recipeType: RecipeTypeEnum
    peopleCount: int = 1

    class Config:
        from_attributes = True


class ForkedRecipeRequestModel(BaseModel):
    recipeName: Optional[str] = None
    description: Optional[str] = None
    recipeType: RecipeTypeEnum
    peopleCount: Optional[int] = None
