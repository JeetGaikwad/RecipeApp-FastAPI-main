from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr
from helper.validation_helper import ValidationHelper
from datetime import datetime

class UserVerification(BaseModel):
    password: str
    new_password: str


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
