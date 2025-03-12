# Importing libraries
from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.forked_recipe_controller import ForkedRecipeController
from dtos.forked_recipe_models import ForkedRecipeRequestModel
from config.constants import Constants

# Declaring router
forked_recipe = APIRouter(tags=["Forked-Recipe"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@forked_recipe.get("/forked-recipes")
async def get_all_forked_recipes(user: user_dependency):
    return ForkedRecipeController.get_all_forked_recipes(user.id)


@forked_recipe.get("/forked-recipes/{forked_id}")
async def get_forked_recipe_by_id(user: user_dependency, forked_id: int):
    return ForkedRecipeController.get_forked_recipe_by_id(user.id, forked_id)


@forked_recipe.post("/fork-recipe/{recipe_id}")
async def add_forked_recipe(user: user_dependency, recipe_id: int):
    return ForkedRecipeController.add_forked_recipe(user.id, recipe_id)


@forked_recipe.put("/{forked_id}")
async def update_forked_recipe(
    user: user_dependency, forked_id: int, request: ForkedRecipeRequestModel
):
    return ForkedRecipeController.update_forked_recipe(user.id, forked_id, request)


@forked_recipe.delete("/{forked_id}")
async def delete_forked_recipe(user: user_dependency, forked_id: int):
    return ForkedRecipeController.delete_forked_recipe(user.id, forked_id)
