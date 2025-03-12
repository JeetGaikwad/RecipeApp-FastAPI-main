# Importing libraries
from dtos.base_response_model import BaseResponseModel
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from models.forked_recipe_table import ForkedRecipe
from models.recipe_table import Recipes
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper
from dtos.forked_recipe_models import (
    ForkedRecipeResponseModel,
    ForkedRecipeRequestModel,
)
from dtos.recipe_models import RecipeTypeEnum


class ForkedRecipeController:

    @staticmethod
    def get_all_forked_recipes(user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipes = (
                    session.query(ForkedRecipe)
                    .filter(ForkedRecipe.userId == user_id)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        ForkedRecipeResponseModel.model_validate(recipe).model_dump(
                            exclude={"userId"}
                        )
                        for recipe in recipes
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_forked_recipe_by_id(user_id: int, forked_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = (
                    session.query(ForkedRecipe)
                    .filter(
                        ForkedRecipe.userId == user_id, ForkedRecipe.id == forked_id
                    )
                    .first()
                )

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=ForkedRecipeResponseModel.model_validate(recipe).model_dump(
                        exclude={"userId"}
                    ),
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def add_forked_recipe(user_id: int, recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                exisitng_recipe = (
                    session.query(Recipes).filter(Recipes.id == recipe_id).first()
                )

                if not exisitng_recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                forked_recipe = ForkedRecipe(
                    userId=user_id,
                    recipeId=recipe_id,
                    recipeName=exisitng_recipe.recipeName,
                    description=exisitng_recipe.description,
                    recipeType=exisitng_recipe.recipeType,
                    peopleCount=exisitng_recipe.peopleCount,
                )

                session.add(forked_recipe)

                exisitng_recipe.forkedCount += 1

                session.commit()
                session.refresh(forked_recipe)
                session.refresh(exisitng_recipe)

                return APIHelper.send_success_response(
                    data=ForkedRecipeResponseModel.model_validate(
                        forked_recipe
                    ).model_dump(),
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def update_forked_recipe(
        user_id: int, forked_id: int, update_request: ForkedRecipeRequestModel
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                exisitng_fork = (
                    session.query(ForkedRecipe)
                    .filter(
                        ForkedRecipe.id == forked_id,
                        ForkedRecipe.userId == user_id,
                    )
                    .first()
                )

                if not exisitng_fork:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                exisitng_fork.recipeName = (
                    update_request.recipeName or exisitng_fork.recipeName
                )
                exisitng_fork.description = (
                    update_request.description or exisitng_fork.description
                )
                exisitng_fork.recipeType = (
                    RecipeTypeEnum(update_request.recipeType)
                    or exisitng_fork.recipeType
                )
                exisitng_fork.peopleCount = (
                    update_request.peopleCount or exisitng_fork.peopleCount
                )

                session.add(exisitng_fork)
                session.commit()
                session.refresh(exisitng_fork)

                return APIHelper.send_success_response(
                    data=ForkedRecipeResponseModel.model_validate(
                        exisitng_fork
                    ).model_dump(),
                    successMessageKey="translations.RECIPE_UPDATED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_forked_recipe(user_id: int, forked_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                existing_fork = (
                    session.query(ForkedRecipe)
                    .filter(
                        ForkedRecipe.id == forked_id,
                        ForkedRecipe.userId == user_id,
                    )
                    .first()
                )

                if not existing_fork:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                recipe = (
                    session.query(Recipes)
                    .filter(Recipes.id == existing_fork.recipeId)
                    .first()
                )

                session.query(ForkedRecipe).filter(
                    ForkedRecipe.id == forked_id
                ).delete()

                recipe.forkedCount -= 1 if recipe.forkedCount > 0 else 0

                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
