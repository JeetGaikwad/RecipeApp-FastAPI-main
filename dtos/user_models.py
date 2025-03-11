from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr
from helper.validation_helper import ValidationHelper
from datetime import datetime
from .auth_models import UserRoleEnum


class UserVerification(BaseModel):
    password: str
    new_password: str


class CreateUserModel(BaseModel):
    email: EmailStr
    username: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    profilePhoto: Optional[str] = None
    dateOfBirth: Optional[datetime] = None
    phoneNumber: Optional[str] = None
    password: str
    role: UserRoleEnum = UserRoleEnum.user

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return ValidationHelper.is_valid_email(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return ValidationHelper.is_valid_password(v)

    @field_validator("phoneNumber")
    @classmethod
    def validate_phone(cls, v):
        return ValidationHelper.is_mobile(v)


class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    profilePhoto: Optional[str] = None
    dateOfBirth: Optional[datetime] = None
    phoneNumber: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return ValidationHelper.is_valid_email(v)

    @field_validator("phoneNumber")
    @classmethod
    def validate_phone(cls, v):
        return ValidationHelper.is_mobile(v)
