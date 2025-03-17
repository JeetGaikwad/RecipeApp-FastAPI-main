# Importing libraries
from dtos.base_response_model import BaseResponseModel
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from models.recipe_table import Recipes
from models.wishlist_table import Wishlist
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper
from dtos.wishlist_models import (
    VisibilityEnum,
    WishlistResponse,
    WishlistRequest,
    WishlistUpdateRequest,
)


class WishlistController:

    @staticmethod
    def get_all_public_wishlist(user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                wishlists = (
                    session.query(Wishlist)
                    .filter(Wishlist.visibility == VisibilityEnum.public)
                    .all()
                )

                if not wishlists:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.WISHLIST_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        WishlistResponse.model_validate(w).model_dump()
                        for w in wishlists
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_user_wishlist(user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                wishlists = (
                    session.query(Wishlist).filter(Wishlist.userId == user_id).all()
                )

                if not wishlists:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.WISHLIST_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        WishlistResponse.model_validate(w).model_dump()
                        for w in wishlists
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def add_wishlist(user_id: int, request: WishlistRequest):
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe_id = request.recipeId
                visibility = request.visibility

                recipe = (
                    session.query(Recipes)
                    .filter(
                        Recipes.id == recipe_id,
                        Recipes.isDeleted == False,
                        Recipes.isHide == False,
                    )
                    .first()
                )

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                existing_wishlist = (
                    session.query(Wishlist)
                    .filter(Wishlist.userId == user_id, Wishlist.recipeId == recipe_id)
                    .first()
                )

                if existing_wishlist:
                    existing_wishlist.visibility = visibility
                    session.commit()
                    session.refresh(existing_wishlist)
                    return APIHelper.send_success_response(
                        data=WishlistResponse.model_validate(
                            existing_wishlist
                        ).model_dump(),
                        successMessageKey="translations.WISHLIST_UPDATED",
                    )

                new_wishlist = Wishlist(
                    userId=user_id, recipeId=recipe_id, visibility=visibility
                )

                session.add(new_wishlist)
                session.commit()
                session.refresh(new_wishlist)

                return APIHelper.send_success_response(
                    data=WishlistResponse.model_validate(new_wishlist).model_dump(),
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def update_wishlist_visibility(
        user_id: int, recipe_id: int, request: WishlistUpdateRequest
    ):
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                wishlist_entry = (
                    session.query(Wishlist)
                    .filter(Wishlist.userId == user_id, Wishlist.recipeId == recipe_id)
                    .first()
                )

                if not wishlist_entry:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.WISHLIST_NOT_FOUND"
                    )

                wishlist_entry.visibility = request.visibility

                session.commit()
                session.refresh(wishlist_entry)

                return APIHelper.send_success_response(
                    data=WishlistResponse.model_validate(wishlist_entry).model_dump(),
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_wishlist(user_id: int, recipe_id: int):
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(user_id)
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                wishlist_entry = (
                    session.query(Wishlist)
                    .filter(Wishlist.userId == user_id, Wishlist.recipeId == recipe_id)
                    .first()
                )

                if not wishlist_entry:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.WISHLIST_NOT_FOUND"
                    )

                session.delete(wishlist_entry)
                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
