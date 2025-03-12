from pydantic import BaseModel
from typing import Optional
from enum import Enum


class RecipeTypeEnum(str, Enum):
    veg = "veg"
    nonveg = "nonveg"


class RecipeResponseModel(BaseModel):
    id: int
    userId: int
    recipeName: str
    description: str
    recipeType: RecipeTypeEnum
    peopleCount: int
    likesCount: int
    forkedCount: int

    class Config:
        from_attributes = True


class RecipeRequestModel(BaseModel):
    recipeName: str
    description: Optional[str] = None
    recipeType: RecipeTypeEnum
    peopleCount: int = 1
