# Importing libraries
from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.admin_controller import AdminController
from config.constants import Constants

# Declaring router
admin = APIRouter(tags=["Admin"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@admin.get("/admin/recipes")
async def get_all_recipes(
    user: user_dependency, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return AdminController.get_all_recipes(user.id, page, size)


@admin.put("/admin/recipes/{recipe_id}/hide")
async def hide_recipes(user: user_dependency, recipe_id: int):
    return AdminController.hide_recipes(user.id, recipe_id)


@admin.put("/admin/recipes/{recipe_id}/show")
async def show_recipes(user: user_dependency, recipe_id: int):
    return AdminController.show_recipes(user.id, recipe_id)


@admin.delete("/admin/recipes/{recipe_id}")
async def delete_recipe(user: user_dependency, recipe_id: int):
    return AdminController.delete_recipe(user.id, recipe_id)


@admin.get("/admin/users")
async def get_all_users(
    user: user_dependency, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return AdminController.get_all_users(user.id, page, size)


@admin.put("/admin/users/{user_id}/block")
async def block_user(user: user_dependency, user_id: int):
    return AdminController.block_user(user.id, user_id)


@admin.put("/admin/users/{user_id}/unblock")
async def unblock_user(user: user_dependency, user_id: int):
    return AdminController.unblock_user(user.id, user_id)


@admin.delete("/admin/users/{user_id}")
async def delete_user(user: user_dependency, user_id: int):
    return AdminController.delete_user(user.id, user_id)


@admin.delete("/admin/comments/{comment_id}")
async def delete_comment(user: user_dependency, comment_id: int):
    return AdminController.delete_comment(user.id, comment_id)
