# Importing libraries
from dtos.base_response_model import BaseResponseModel
from dtos.recipe_ingredient_models import (
    RecipeIngredientResponseModel,
    IngredientBaseModel,
    RecipeIngredientRequest,
)
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from models.recipe_table import Recipes
from models.recipe_ingredients_table import RecipeIngredient, Ingredient
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper


class RecipeIngredientController:

    @staticmethod
    def get_recipe_ingredients(recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                ingredients = (
                    session.query(
                        Ingredient.ingredientName,
                        RecipeIngredient.quantity,
                        RecipeIngredient.unit,
                    )
                    .join(
                        RecipeIngredient, Ingredient.id == RecipeIngredient.ingredientId
                    )
                    .filter(RecipeIngredient.recipeId == recipe_id)
                    .all()
                )

                if not ingredients:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.INGREDIENT_NOT_FOUND"
                    )

                ingredient_data = [
                    {"ingredientName": name, "quantity": quantity, "unit": unit}
                    for name, quantity, unit in ingredients
                ]

                return APIHelper.send_success_response(
                    data=[
                        RecipeIngredientResponseModel.model_validate(data).model_dump()
                        for data in ingredient_data
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_ingredient_by_name(ingredient_name: str) -> BaseResponseModel:
        try:
            ingredient_name = ingredient_name.strip()

            with SessionLocal() as session:

                ingredient_search = (
                    session.query(Ingredient)
                    .filter(
                        (Ingredient.ingredientName.ilike(f"%{ingredient_name}%")),
                    )
                    .all()
                )

                if not ingredient_search:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.INGREDIENT_NOT_FOUND"
                    )

                ingredient_data = [
                    {"ingredientName": ingredient.ingredientName}
                    for ingredient in ingredient_search
                ]

                return APIHelper.send_success_response(
                    data=[
                        IngredientBaseModel.model_validate(ingredient).model_dump()
                        for ingredient in ingredient_data
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def add_recipe_ingredient(
        user_id: int,
        recipe_id: int,
        ingredient_request: IngredientBaseModel,
        recipe_ing_request: RecipeIngredientRequest,
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                existing_recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.userId == user_id,
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not existing_recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                ingredient = (
                    session.query(Ingredient)
                    .filter(
                        Ingredient.ingredientName
                        == ingredient_request.ingredientName.capitalize()
                    )
                    .first()
                )

                if not ingredient:
                    ingredient_model = Ingredient(
                        ingredientName=ingredient_request.ingredientName.capitalize()
                    )
                    session.add(ingredient_model)
                    session.commit()
                    session.refresh(ingredient_model)
                    ingredient = ingredient_model

                recipe_ingredient = RecipeIngredient(
                    ingredientId=ingredient.id,
                    recipeId=existing_recipe.id,
                    quantity=recipe_ing_request.quantity,
                    unit=recipe_ing_request.unit,
                )

                session.add(recipe_ingredient)
                session.commit()
                session.refresh(recipe_ingredient)

                return APIHelper.send_success_response(
                    successMessageKey="translations.INGREDIENT_ADDED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def update_recipe_ingredient(
        user_id: int,
        recipe_id: int,
        ingredient_id: int,
        recipe_ing_request: RecipeIngredientRequest,
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                existing_recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.userId == user_id,
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not existing_recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                recipe_ingredient = (
                    session.query(RecipeIngredient)
                    .filter(
                        (RecipeIngredient.recipeId == recipe_id)
                        & (RecipeIngredient.ingredientId == ingredient_id)
                    )
                    .first()
                )

                if not recipe_ingredient:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.INGREDIENT_NOT_FOUND"
                    )

                recipe_ingredient.quantity = recipe_ing_request.quantity
                recipe_ingredient.unit = recipe_ing_request.unit

                session.commit()
                session.refresh(recipe_ingredient)

                return APIHelper.send_success_response(
                    successMessageKey="translations.INGREDIENT_UPDATED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_recipe_ingredient(
        user_id: int,
        recipe_id: int,
        ingredient_id: int,
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                existing_recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.userId == user_id,
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not existing_recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                ingredient = (
                    session.query(RecipeIngredient)
                    .filter(
                        RecipeIngredient.recipeId == recipe_id,
                        RecipeIngredient.id == ingredient_id,
                    )
                    .first()
                )

                if not ingredient:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.INGREDIENT_NOT_FOUND"
                    )

                session.delete(ingredient)
                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
