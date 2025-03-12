# Importing libraries
from dtos.auth_models import Token
from dtos.base_response_model import BaseResponseModel
from helper.token_helper import TokenHelper
from helper.hashing import Hash
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


class AuthController:
    def login(request: OAuth2PasswordRequestForm) -> BaseResponseModel:
        user = Hash.authenticate_user(
            username=request.username, password=request.password
        )
        access_token = TokenHelper.create_access_token({"id": user.id})
        response = Token(access_token=access_token)
        return response
        # return APIHelper.send_success_response(
        #     data=response, successMessageKey="translations.LOGIN_SUCCESS"
        # )
