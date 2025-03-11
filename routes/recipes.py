# Importing libraries
from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.recipe_controller import RecipeController
from dtos.recipe_models import RecipeRequestModel, RecipeTypeEnum
from config.constants import Constants

# Declaring router
recipe = APIRouter(tags=["Recipe"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@recipe.get("/recipes")
async def get_all_recipes(page: int, size: Optional[int] = Constants.PAGE_SIZE):
    return RecipeController.get_all_recipes(page, size)


@recipe.get("/recipes/by-user-id")
async def get_recipes_by_user_id(
    user: user_dependency, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return RecipeController.get_recipes_by_user_id(user.id, page, size)


@recipe.get("/recipes/by-type/{recipe_type}")
async def get_recipes_by_type(
    recipe_type: RecipeTypeEnum, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return RecipeController.get_recipes_by_type(recipe_type, page, size)


@recipe.get("/recipes/by-people-count/{people_count}")
async def get_recipes_by_people_count(
    people_count: int, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return RecipeController.get_recipes_by_people_count(people_count, page, size)


@recipe.get("/recipes/by-likes/")
async def get_recipes_by_like(page: int, size: Optional[int] = Constants.PAGE_SIZE):
    return RecipeController.get_recipes_by_like(page, size)


@recipe.get("/recipes/search/")
async def search_recipes(
    query: str, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return RecipeController.search_recipes(query, page, size)


@recipe.get("/recipes/{recipe_id}")
async def get_recipe_by_id(recipe_id: int):
    return RecipeController.get_recipe_by_id(recipe_id)


@recipe.post("/recipes/recipe")
async def create_recipe(user: user_dependency, request: RecipeRequestModel):
    return RecipeController.create_recipe(user.id, request)


@recipe.post("/recipes/{recipe_id}/like")
async def like_recipe(recipe_id: int, user: user_dependency):
    return RecipeController.like_recipe(recipe_id, user.id)


@recipe.post("/recipes/{recipe_id}/unlike")
async def unlike_recipe(recipe_id: int, user: user_dependency):
    return RecipeController.unlike_recipe(recipe_id, user.id)


@recipe.put("/recipes/{recipe_id}")
async def update_recipe(
    recipe_id: int, user: user_dependency, request: RecipeRequestModel
):
    return RecipeController.update_recipe(recipe_id, user.id, request)


@recipe.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, user: user_dependency):
    return RecipeController.delete_recipe(recipe_id, user.id)
