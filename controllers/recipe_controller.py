# Importing libraries
from dtos.base_response_model import BaseResponseModel
from dtos.recipe_models import RecipeResponseModel, RecipeRequestModel, RecipeTypeEnum
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from helper.hashing import Hash
from models.recipe_table import Recipes
from models.recipe_likes_table import RecipeLike
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper


class RecipeController:

    @staticmethod
    def get_all_recipes(page: int, size: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                recipes = (
                    session.query(Recipes)
                    .filter(Recipes.isDeleted.is_(False), Recipes.isHide.is_(False))
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeResponseModel.model_validate(recipe).model_dump()
                        for recipe in recipes
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_recipe_by_id(recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=RecipeResponseModel.model_validate(recipe).model_dump(),
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_recipes_by_user_id(user_id: int, page: int, size: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipes = (
                    session.query(Recipes)
                    .filter(
                        Recipes.userId == user_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeResponseModel.model_validate(recipe).model_dump(
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
    def get_recipes_by_type(
        recipe_type: RecipeTypeEnum, page: int, size: int
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                recipes = (
                    session.query(Recipes)
                    .filter(
                        Recipes.recipeType == recipe_type,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeResponseModel.model_validate(recipe).model_dump()
                        for recipe in recipes
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_recipes_by_people_count(
        people_count: int, page: int, size: int
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                recipes = (
                    session.query(Recipes)
                    .filter(
                        Recipes.peopleCount == people_count,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeResponseModel.model_validate(recipe).model_dump(
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
    def search_recipes(search: str, page: int, size: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                recipes = (
                    session.query(Recipes)
                    .filter(
                        (Recipes.recipeName.like(f"%{search}%"))
                        | (Recipes.description.like(f"%{search}%")),
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeResponseModel.model_validate(recipe).model_dump(
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
    def get_recipes_by_like(page: int, size: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                recipes = (
                    session.query(Recipes)
                    .filter(
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .order_by(Recipes.likesCount.desc())
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not recipes:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeResponseModel.model_validate(recipe).model_dump(
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
    def create_recipe(user_id: int, request: RecipeRequestModel) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe_model = Recipes(
                    userId=user_id,
                    recipeName=request.recipeName,
                    description=request.description,
                    recipeType=request.recipeType,
                    peopleCount=request.peopleCount,
                )

                session.add(recipe_model)
                session.commit()
                session.refresh(recipe_model)

                return APIHelper.send_success_response(
                    data=RecipeResponseModel.model_validate(recipe_model).model_dump(),
                    successMessageKey="translations.RECIPE_CREATED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def like_recipe(recipe_id: int, user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                existing_like = (
                    session.query(RecipeLike)
                    .filter(
                        (RecipeLike.userId == user_id)
                        & (RecipeLike.recipeId == recipe_id)
                    )
                    .first()
                )

                if existing_like:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.ALREADY_LIKED"
                    )

                new_like = RecipeLike(userId=user_id, recipeId=recipe_id)

                session.add(new_like)

                recipe.likesCount += 1

                session.commit()
                session.refresh(new_like)
                session.refresh(recipe)

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def unlike_recipe(recipe_id: int, user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                existing_like = (
                    session.query(RecipeLike)
                    .filter(
                        (RecipeLike.userId == user_id)
                        & (RecipeLike.recipeId == recipe_id)
                    )
                    .first()
                )

                if not existing_like:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.NOT_LIKED"
                    )

                session.delete(existing_like)

                recipe.likesCount -= 1

                session.commit()
                session.refresh(recipe)

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def update_recipe(
        recipe_id: int, user_id: int, update_request: RecipeRequestModel
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe_model = (
                    session.query(Recipes)
                    .filter(
                        Recipes.userId == user_id,
                        Recipes.id == recipe_id,
                        Recipes.isDeleted.is_(False),
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not recipe_model:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                recipe_model.recipeName = update_request.recipeName
                recipe_model.description = update_request.description
                recipe_model.recipeType = RecipeTypeEnum(update_request.recipeType)
                recipe_model.peopleCount = update_request.peopleCount

                session.add(recipe_model)
                session.commit()
                session.refresh(recipe_model)

                return APIHelper.send_success_response(
                    data=RecipeResponseModel.model_validate(recipe_model).model_dump(),
                    successMessageKey="translations.RECIPE_UPDATED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_recipe(recipe_id: int, user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe_model = (
                    session.query(Recipes)
                    .filter(
                        Recipes.userId == user_id,
                        Recipes.id == recipe_id,
                        Recipes.isHide.is_(False),
                    )
                    .first()
                )

                if not recipe_model:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                recipe_model.isDeleted = True

                session.add(recipe_model)
                session.commit()
                session.refresh(recipe_model)

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
