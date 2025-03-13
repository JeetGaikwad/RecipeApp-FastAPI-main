# Importing libraries
from typing import Annotated
from fastapi import APIRouter, Depends
from controllers.user_controller import UserController, CreateUserModel
from helper.token_helper import TokenHelper
from dtos.user_models import UserVerification, UpdateUserRequest

# Declaring router
user = APIRouter(tags=["User"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@user.post("/create/user")
async def create_user(request: CreateUserModel):
    return UserController.create_user(request)


@user.get("/user")
async def get_user(current_user: user_dependency):
    return UserController.get_user(current_user.id)


@user.post("/user/follow/{followee_id}")
async def follow_user(followee_id: int, current_user: user_dependency):
    return UserController.follow_user(current_user.id, followee_id)


@user.post("/user/unfollow/{followee_id}")
async def unfollow_user(followee_id: int, current_user: user_dependency):
    return UserController.unfollow_user(current_user.id, followee_id)


@user.put("/user/change-password")
async def change_password(
    request: UserVerification,
    current_user: user_dependency,
):
    return UserController.change_password(
        current_user.id, request.password, request.new_password
    )


@user.put("/profile-update")
async def update_profile(
    request: UpdateUserRequest,
    current_user: user_dependency,
):
    return UserController.update_profile(current_user.id, request)
