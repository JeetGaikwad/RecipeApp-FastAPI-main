# Importing libraries
from dtos.auth_models import Token
from dtos.base_response_model import BaseResponseModel
from helper.api_helper import APIHelper
from helper.token_helper import TokenHelper
from helper.hashing import Hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


class AuthController:
    def login(request: OAuth2PasswordRequestForm) -> BaseResponseModel:
        user = Hash.authenticate_user(
            username=request.username, password=request.password
        )
        access_token = TokenHelper.create_access_token(data={"id": user.id})
        response = Token(access_token=access_token, **user.model_dump())
        return APIHelper.send_success_response(
            data=response, successMessageKey="translations.LOGIN_SUCCESS"
        )
