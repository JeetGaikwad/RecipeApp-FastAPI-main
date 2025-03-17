from pydantic import BaseModel
from enum import Enum


class VisibilityEnum(str, Enum):
    private = "private"
    public = "public"


class WishlistRequest(BaseModel):
    recipeId: int
    visibility: VisibilityEnum


class WishlistUpdateRequest(BaseModel):
    visibility: VisibilityEnum


class WishlistResponse(BaseModel):
    id: int
    userId: int
    recipeId: int

    class Config:
        from_attributes = True
