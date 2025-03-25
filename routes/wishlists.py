# Importing libraries
from typing import Annotated, Optional
from fastapi import APIRouter, Depends
from helper.token_helper import TokenHelper
from controllers.wishlist_controller import WishlistController
from dtos.wishlist_models import WishlistRequest, WishlistUpdateRequest
from config.constants import Constants

# Declaring router
wishlist = APIRouter(tags=["Wishlist"])

user_dependency = Annotated[dict, Depends(TokenHelper.get_current_user)]


@wishlist.get("/wishlists/public")
async def get_all_public_wishlist(
    user: user_dependency, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return WishlistController.get_all_public_wishlist(user.id, page, size)


@wishlist.get("/wishlists")
async def get_user_wishlist(
    user: user_dependency, page: int, size: Optional[int] = Constants.PAGE_SIZE
):
    return WishlistController.get_user_wishlist(user.id, page, size)


@wishlist.post("/wishlists")
async def add_wishlist(user: user_dependency, request: WishlistRequest):
    return WishlistController.add_wishlist(user.id, request)


@wishlist.put("/wishlists/{recipe_id}")
async def update_wishlist_visibility(
    user: user_dependency, recipe_id: int, request: WishlistUpdateRequest
):
    return WishlistController.update_wishlist_visibility(user.id, recipe_id, request)


@wishlist.delete("/wishlists/{recipe_id}")
async def delete_wishlist(user: user_dependency, recipe_id: int):
    return WishlistController.delete_wishlist(user.id, recipe_id)
