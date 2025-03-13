# Importing libraries
from dtos.base_response_model import BaseResponseModel
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from models.recipe_table import Recipes
from models.recipe_comments_table import RecipeComment
from sqlalchemy.exc import SQLAlchemyError
from utils.db_helper import DBHelper
from dtos.comment_model import RecipeCommentResponse, CommentRequest


class CommentController:

    @staticmethod
    def get_all_recipe_comments(recipe_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                comments = (
                    session.query(RecipeComment)
                    .filter(RecipeComment.recipeId == recipe_id)
                    .all()
                )

                if not comments:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.COMMENT_NOT_FOUND"
                    )

                return APIHelper.send_success_response(
                    data=[
                        RecipeCommentResponse.model_validate(comment).model_dump()
                        for comment in comments
                    ],
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_recipe_comment_with_replies(
        recipe_id: int, comment_id: int
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                comment = (
                    session.query(RecipeComment)
                    .filter(
                        (RecipeComment.recipeId == recipe_id)
                        & (RecipeComment.id == comment_id)
                    )
                    .first()
                )

                if not comment:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.COMMENT_NOT_FOUND"
                    )

                def get_replies(parent_id):
                    replies = (
                        session.query(RecipeComment)
                        .filter(RecipeComment.parentCommentId == parent_id)
                        .all()
                    )

                    return [
                        {
                            "id": reply.id,
                            "userId": reply.userId,
                            "comment": reply.comment,
                            "replies": get_replies(reply.id),
                        }
                        for reply in replies
                    ]

                comment_data = {
                    "id": comment.id,
                    "userId": comment.userId,
                    "comment": comment.comment,
                    "replies": get_replies(comment.id),
                }

                return APIHelper.send_success_response(
                    data=comment_data,
                    successMessageKey="translations.SUCCESS",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def add_comment(
        user_id: int, recipe_id: int, comment_request: CommentRequest
    ) -> BaseResponseModel:

        try:
            with SessionLocal() as session:

                user = DBHelper.get_user_by_id(user_id)
                if user is None:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe_commented = (
                    session.query(Recipes).filter(Recipes.id == recipe_id).first()
                )

                if not recipe_commented:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.RECIPE_NOT_FOUND"
                    )

                if comment_request.parentCommentId:
                    parent_comment = (
                        session.query(RecipeComment)
                        .filter(
                            (RecipeComment.recipeId == recipe_id)
                            & (RecipeComment.id == comment_request.parentCommentId)
                        )
                        .first()
                    )

                    if not parent_comment:
                        return APIHelper.send_error_response(
                            errorMessageKey="translations.PARENT_COMMENT_NOT_FOUND"
                        )

                new_comment = RecipeComment(
                    userId=user_id,
                    recipeId=recipe_id,
                    comment=comment_request.comment,
                    parentCommentId=comment_request.parentCommentId,
                )

                session.add(new_comment)
                session.commit()
                session.refresh(new_comment)

                return APIHelper.send_success_response(
                    data=RecipeCommentResponse.model_validate(new_comment).model_dump(),
                    successMessageKey="translations.COMMENT_ADDEu",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def update_comment(
        user_id: int, recipe_id: int, comment_id: int, comment_request: CommentRequest
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:

                user = DBHelper.get_user_by_id(user_id)
                if user is None:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                recipe_comment = (
                    session.query(RecipeComment)
                    .filter(
                        (RecipeComment.id == comment_id)
                        & (RecipeComment.userId == user_id)
                        & (RecipeComment.recipeId == recipe_id)
                    )
                    .first()
                )

                if not recipe_comment:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.COMMENT_NOT_FOUND"
                    )

                if not comment_request.comment or comment_request.comment.strip() == "":
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.EMPTY_COMMENT"
                    )

                recipe_comment.comment = comment_request.comment
                session.commit()
                session.refresh(recipe_comment)

                return APIHelper.send_success_response(
                    successMessageKey="translations.COMMENT_UPDATED"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def delete_comment(user_id: int, comment_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:

                user = DBHelper.get_user_by_id(user_id)
                if user is None:
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

                if comment.userId != user_id:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_DELETE"
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
