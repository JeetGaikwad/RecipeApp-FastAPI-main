# Importing libraries
from typing import Annotated
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.cooking_history_controller import CookingHistoryController
from dtos.cooking_history_model import CookingHistoryRequest

# Declaring router
cooking_history = APIRouter(tags=["Cooking-History"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@cooking_history.get("/cooking-history")
async def get_user_cooking_history(user: user_dependency):
    return CookingHistoryController.get_user_cooking_history(user.id)


@cooking_history.post("/cooking-history")
async def add_cooking_history(user: user_dependency, request: CookingHistoryRequest):
    return CookingHistoryController.add_cooking_history(user.id, request.recipe_id)


@cooking_history.delete("/cooking-history/{recipe_id}")
async def delete_cooking_history(user: user_dependency, recipe_id: int):
    return CookingHistoryController.delete_cooking_history(user.id, recipe_id)
