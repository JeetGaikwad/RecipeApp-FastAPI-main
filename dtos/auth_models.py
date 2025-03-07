from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = 'Bearer'


class AddUserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserModel(BaseModel):
    id: int
    email: EmailStr
    username: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    bio: Optional[str] = None
    profilePhoto: Optional[str] = None
    dateOfBirth: Optional[datetime] = None
    phoneNumber: Optional[str] = None
    role: AddUserRole
