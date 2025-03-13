from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    func,
)
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from config.db_config import Base


class RecipeTypeEnum(str, PyEnum):
    veg = "veg"
    nonveg = "nonveg"


class Recipes(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipeName = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    recipeType = Column(Enum(RecipeTypeEnum), nullable=False)
    peopleCount = Column(Integer, nullable=False, server_default="1")
    likesCount = Column(Integer, nullable=False, server_default="0")
    forkedCount = Column(Integer, nullable=False, server_default="0")
    isDeleted = Column(Boolean, nullable=False, server_default="0")
    isHide = Column(Boolean, nullable=False, server_default="0")
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )
    deletedAt = Column(DateTime, nullable=True)

    likes = relationship(
        "RecipeLike", back_populates="recipe", cascade="all, delete-orphan"
    )

    forked_recipes = relationship(
        "ForkedRecipe",
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    recipe_ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe_ing",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    comments = relationship(
        "RecipeComment",
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
