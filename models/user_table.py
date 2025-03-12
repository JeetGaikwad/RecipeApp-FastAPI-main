from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db_config import Base

UserRoleEnum = Enum("user", "admin", name="user_role_enum")


# Initializing
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    firstName = Column(String(255))
    lastName = Column(String(255))
    bio = Column(String(500))
    profilePhoto = Column(String(255), nullable=True)
    dateOfBirth = Column(DateTime)
    phoneNumber = Column(String(30))
    password = Column(String(300), nullable=False)
    role = Column(UserRoleEnum, nullable=False, server_default="user")
    followersCount = Column(Integer, nullable=False, server_default="0")
    followingCount = Column(Integer, nullable=False, server_default="0")
    isBlocked = Column(Boolean, nullable=False, server_default="false")
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    recipe_likes = relationship(
        "RecipeLike", back_populates="user", cascade="all, delete-orphan"
    )

    forked_recipes = relationship(
        "ForkedRecipe",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
