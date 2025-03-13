# Importing libraries
from typing import Annotated
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.recipe_ingredient_controller import RecipeIngredientController
from dtos.recipe_ingredient_models import IngredientBaseModel, RecipeIngredientRequest

ingredient = APIRouter(tags=["Recipe-Ingredients"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@ingredient.get("/ingredients/search")
async def get_ingredient_by_name(ingredient_name: str):
    return RecipeIngredientController.get_ingredient_by_name(ingredient_name)


@ingredient.get("/ingredients/{recipe_id}")
async def get_recipe_ingredients(recipe_id: int):
    return RecipeIngredientController.get_recipe_ingredients(recipe_id)


@ingredient.post("/ingredients/{recipe_id}/ingredient")
async def add_recipe_ingredient(
    recipe_id: int,
    user: user_dependency,
    ingredient_request: IngredientBaseModel,
    recipe_ing_request: RecipeIngredientRequest,
):
    return RecipeIngredientController.add_recipe_ingredient(
        user.id, recipe_id, ingredient_request, recipe_ing_request
    )


@ingredient.put("/ingredients/{recipe_id}/ingredient/{ingredient_id}")
async def update_recipe_ingredient(
    recipe_id: int,
    user: user_dependency,
    ingredient_id: int,
    recipe_ing_request: RecipeIngredientRequest,
):
    return RecipeIngredientController.update_recipe_ingredient(
        user.id, recipe_id, ingredient_id, recipe_ing_request
    )


@ingredient.delete("/ingredients/{recipe_id}/ingredient/{ingredient_id}")
async def delete_recipe_ingredient(
    recipe_id: int,
    user: user_dependency,
    ingredient_id: int,
):
    return RecipeIngredientController.delete_recipe_ingredient(
        user.id, recipe_id, ingredient_id
    )
