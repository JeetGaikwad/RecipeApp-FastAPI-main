# Importing libraries
from dtos.auth_models import UserModel
from dtos.base_response_model import BaseResponseModel
from dtos.user_models import UpdateUserRequest, CreateUserModel
from helper.api_helper import APIHelper
from config.db_config import SessionLocal
from helper.hashing import Hash
from models.user_table import Users
from models.follow_table import Follows
from sqlalchemy.exc import SQLAlchemyError


class UserController:

    @staticmethod
    def create_user(user_data: CreateUserModel) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                existing_user = (
                    session.query(Users)
                    .filter(
                        (Users.email == user_data.email)
                        | (Users.username == user_data.username)
                    )
                    .first()
                )

                if existing_user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_ALREADY_EXISTS"
                    )

                hashed_password = Hash.get_hash(user_data.password)

                new_user = Users(
                    email=user_data.email,
                    username=user_data.username,
                    firstName=user_data.firstName,
                    lastName=user_data.lastName,
                    bio=user_data.bio,
                    profilePhoto=user_data.profilePhoto,
                    dateOfBirth=user_data.dateOfBirth,
                    phoneNumber=user_data.phoneNumber,
                    password=hashed_password,
                    role=user_data.role,
                )

                session.add(new_user)
                session.commit()
                session.refresh(new_user)

                return APIHelper.send_success_response(
                    successMessageKey="translations.USER_CREATED"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def get_user(user_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = session.query(Users).filter(Users.id == user_id).first()
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )
                return APIHelper.send_success_response(
                    data=UserModel(
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
                    ),
                    successMessageKey="translations.USER_FOUND",
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def follow_user(user_id: int, followee_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = session.query(Users).filter(Users.id == user_id).first()
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                follower_id = user_id

                if followee_id == follower_id:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.CANNOT_FOLLOW_YOURSELF"
                    )

                existing_follow = (
                    session.query(Follows)
                    .filter(
                        (Follows.followerId == follower_id)
                        & (Follows.followeeId == followee_id)
                    )
                    .first()
                )

                if existing_follow:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.ALREADY_FOLLOW"
                    )

                new_follower = Follows(followerId=follower_id, followeeId=followee_id)
                session.add(new_follower)

                session.query(Users).filter(Users.id == follower_id).update(
                    {"followingCount": Users.followingCount + 1}
                )
                session.query(Users).filter(Users.id == followee_id).update(
                    {"followersCount": Users.followersCount + 1}
                )

                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def unfollow_user(user_id: int, followee_id: int) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = session.query(Users).filter(Users.id == user_id).first()
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                follower_id = user_id

                follow = (
                    session.query(Follows)
                    .filter(
                        (Follows.followerId == follower_id)
                        & (Follows.followeeId == followee_id)
                    )
                    .first()
                )

                if not follow:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.DO_NOT_FOLLOW"
                    )

                session.delete(follow)

                follower = session.query(Users).filter(Users.id == follower_id).first()
                followee = session.query(Users).filter(Users.id == followee_id).first()

                follower_following_count = max(follower.followingCount - 1, 0)
                followee_followers_count = max(followee.followersCount - 1, 0)

                session.query(Users).filter(Users.id == follower_id).update(
                    {"followingCount": (follower_following_count)}
                )
                session.query(Users).filter(Users.id == followee_id).update(
                    {"followersCount": (followee_followers_count)}
                )

                session.commit()

                return APIHelper.send_success_response(
                    successMessageKey="translations.SUCCESS"
                )

        except SQLAlchemyError:
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def change_password(
        user_id: int, current_password: str, new_password: str
    ) -> BaseResponseModel:
        try:
            with SessionLocal() as session:
                user = session.query(Users).filter(Users.id == user_id).first()
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.UNAUTHORIZE_USER"
                    )

                if not Hash.verify(current_password, user.password):
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.INVALID_PASSWORD"
                    )

                user.password = Hash.get_hash(new_password)
                session.commit()
                session.refresh(user)

                return APIHelper.send_success_response(
                    successMessageKey="translations.PASSWORD_CHANGED"
                )

        except SQLAlchemyError:
            session.rollback()
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )

    @staticmethod
    def update_profile(
        user_id: int, update_user: UpdateUserRequest
    ) -> BaseResponseModel:

        try:
            with SessionLocal() as session:
                user = session.query(Users).filter(Users.id == user_id).first()
                if not user:
                    return APIHelper.send_error_response(
                        errorMessageKey="translations.USER_NOT_FOUND"
                    )

                user.email = update_user.email or user.email
                user.username = update_user.username or user.username
                user.firstName = update_user.firstName or user.firstName
                user.lastName = update_user.lastName or user.lastName
                user.bio = update_user.bio or user.bio
                user.profilePhoto = update_user.profilePhoto or user.profilePhoto
                user.dateOfBirth = update_user.dateOfBirth or user.dateOfBirth
                user.phoneNumber = update_user.phoneNumber or user.phoneNumber

                session.commit()
                session.refresh(user)

                return APIHelper.send_success_response(
                    successMessageKey="translations.PROFILE_UPDATED"
                )
        except SQLAlchemyError:
            session.rollback()
            return APIHelper.send_error_response(
                errorMessageKey="translations.DATABASE_ERROR"
            )
