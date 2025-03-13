# Importing libraries
from dtos.base_response_model import BaseResponseModel
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from models.recipe_table import Recipes
from models.cooking_history_table import CookingHistory
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper
from dtos.cooking_history_model import CookingHistoryResponse
from datetime import datetime


class CookingHistoryController:

    @staticmethod
    def get_user_cooking_history(user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                histories = (
                    session.query(
                        CookingHistory,
                        Recipes.recipeName,
                        Recipes.description,
                        Recipes.likesCount,
                    )
                    .join(Recipes, CookingHistory.recipeId == Recipes.id)
                    .filter(CookingHistory.userId == user_id)
                    .order_by(CookingHistory.createdAt.desc())
                    .all()
                )

                if not histories:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.HISTORY_NOT_FOUND"
                    )

                cooked_history = [
                    CookingHistoryResponse(
                        userId=user_id,
                        recipeId=history.CookingHistory.recipeId,
                        recipeName=history.recipeName,
                        recipeDescription=history.description,
                        likesCount=history.likesCount,
                        createdAt=history.CookingHistory.createdAt,
                    )
                    for history in histories
                ]

                return APIHelper.send_success_response(
                    data=cooked_history,
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def add_cooking_history(user_id: int, recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = session.query(Recipes).filter(Recipes.id == recipe_id).first()
                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                existing_history = (
                    session.query(CookingHistory)
                    .filter(
                        CookingHistory.userId == user_id,
                        CookingHistory.recipeId == recipe_id,
                    )
                    .first()
                )

                if existing_history:
                    # Update the createdAt timestamp to now
                    existing_history.createdAt = datetime.now()
                else:
                    # Create new history record
                    existing_history = CookingHistory(
                        userId=user_id, recipeId=recipe_id
                    )
                    session.add(existing_history)

                session.commit()

                # Return response with recipe details
                response_data = {
                    "userId": user_id,
                    "recipeId": recipe_id,
                    "recipeName": recipe.recipeName,  # Fetching from Recipes table
                    "createdAt": existing_history.createdAt,
                }

                return APIHelper.send_success_response(
                    data=response_data,
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_cooking_history(user_id: int, recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                history = (
                    session.query(CookingHistory)
                    .filter(
                        CookingHistory.userId == user_id,
                        CookingHistory.recipeId == recipe_id,
                    )
                    .first()
                )

                if not history:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.HISTORY_NOT_FOUND"
                    )

                session.delete(history)
                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
