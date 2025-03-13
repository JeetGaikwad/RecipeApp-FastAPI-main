# Importing libraries
from typing import Annotated
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.comment_controller import CommentController
from dtos.comment_model import CommentRequest

# Declaring router
recipe_comment = APIRouter(tags=["Recipe-Comments"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@recipe_comment.get("/comments/{recipe_id}")
async def get_all_recipe_comments(recipe_id: int):
    return CommentController.get_all_recipe_comments(recipe_id)


@recipe_comment.get("/comments/{recipe_id}/{comment_id}")
async def get_recipe_comment_with_replies(recipe_id: int, comment_id: int):
    return CommentController.get_recipe_comment_with_replies(recipe_id, comment_id)


@recipe_comment.post("/comments/{recipe_id}")
async def add_comment(user: user_dependency, recipe_id: int, request: CommentRequest):
    return CommentController.add_comment(user.id, recipe_id, request)


@recipe_comment.put("/comments/{recipe_id}/{comment_id}")
async def update_comment(
    user: user_dependency, recipe_id: int, comment_id: int, request: CommentRequest
):
    return CommentController.update_comment(user.id, recipe_id, comment_id, request)


@recipe_comment.delete("/comments/{comment_id}")
async def delete_comment(user: user_dependency, comment_id: int):
    return CommentController.delete_comment(user.id, comment_id)
