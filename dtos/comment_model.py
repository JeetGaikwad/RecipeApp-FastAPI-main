from pydantic import BaseModel
from typing import Optional


class RecipeCommentResponse(BaseModel):
    userId: int
    comment: str
    parentCommentId: Optional[int] = None

    class Config:
        from_attributes = True


class CommentRequest(BaseModel):
    comment: str
    parentCommentId: Optional[int] = None
