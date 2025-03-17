# Importing libraries
from dtos.base_response_model import BaseResponseModel
from dtos.recipe_models import RecipeResponseModel
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from models.recipe_table import Recipes
from models.user_table import Users
from models.recipe_comments_table import RecipeComment
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper
from dtos.user_models import UserRoleEnum
from dtos.auth_models import UserModel


class AdminController:

    @staticmethod
    def get_all_recipes(admin_id: int, page: int, size: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipes = (
                    session.query(Recipes).offset((page - 1) * size).limit(size).all()
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
    def hide_recipes(admin_id: int, recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = session.query(Recipes).filter(Recipes.id == recipe_id).first()

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                if recipe.isHide:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_ALREADY_HIDDEN"
                    )

                recipe.isHide = True

                session.commit()
                session.refresh(recipe)

                return APIHelper.send_success_response(
                    successMessageKey="translations.RECIPE_HIDE",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def show_recipes(admin_id: int, recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = session.query(Recipes).filter(Recipes.id == recipe_id).first()

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                if not recipe.isHide:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_ALREADY_SHOW"
                    )

                recipe.isHide = False

                session.commit()
                session.refresh(recipe)

                return APIHelper.send_success_response(
                    successMessageKey="translations.RECIPE_SHOW",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_recipe(admin_id: int, recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe = session.query(Recipes).filter(Recipes.id == recipe_id).first()

                if not recipe:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                if recipe.isDeleted:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_DELETE_STAGE"
                    )

                recipe.isDeleted = True

                session.commit()
                session.refresh(recipe)

                return APIHelper.send_success_response(
                    successMessageKey="translations.RECIPE_DELETE",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_all_users(admin_id: int, page: int, size: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                users = (
                    session.query(Users)
                    .order_by(Users.createdAt.desc())
                    .offset((page - 1) * size)
                    .limit(size)
                    .all()
                )

                if not users:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        UserModel(
                            id=user.id,
                            email=user.email,
                            username=user.username,
                            firstName=user.firstName,
                            lastName=user.lastName,
                            bio=user.bio,
                            profilePhoto=user.profilePhoto,
                            dateOfBirth=user.dateOfBirth,
                            phoneNumber=user.phoneNumber,
                            role=user.role,
                            followersCount=user.followersCount,
                            followingCount=user.followingCount,
                        )
                        for user in users
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def block_user(admin_id: int, user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                exisitng_user = session.query(Users).filter(Users.id == user_id).first()

                if not exisitng_user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_NOT_FOUND"
                    )

                if exisitng_user.isBlocked:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.ALREADY_BLOCKED"
                    )

                exisitng_user.isBlocked = True

                session.commit()
                session.refresh(exisitng_user)

                return APIHelper.send_success_response(
                    successMessageKey="translations.USER_BLOCKED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def unblock_user(admin_id: int, user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                exisitng_user = session.query(Users).filter(Users.id == user_id).first()

                if not exisitng_user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_NOT_FOUND"
                    )

                if not exisitng_user.isBlocked:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.ALREADY_UNBLOCKED"
                    )

                exisitng_user.isBlocked = False

                session.commit()
                session.refresh(exisitng_user)

                return APIHelper.send_success_response(
                    successMessageKey="translations.USER_UNBLOCKED",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_user(admin_id: int, user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                exisitng_user = session.query(Users).filter(Users.id == user_id).first()

                if not exisitng_user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_NOT_FOUND"
                    )

                session.delete(exisitng_user)
                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.USER_DELETED",
                )

        except SQLAlchemyError as e:
            print(str(e))  # Log the actual database error
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_comment(admin_id: int, comment_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:

                user = DBHelper.get_user_by_id(admin_id)
                if not user or user.role != UserRoleEnum.admin:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                comment = (
                    session.query(RecipeComment)
                    .filter(RecipeComment.id == comment_id)
                    .first()
                )

                if not comment:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.COMMENT_NOT_FOUND"
                    )

                session.delete(comment)
                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.COMMENT_DELETED"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
