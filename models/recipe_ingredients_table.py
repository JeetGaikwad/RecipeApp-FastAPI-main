from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy.sql import func
from config.db_config import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredientName = Column(String(255), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    recipe_ingredients = relationship(
        "RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan"
    )


class WeightUnitEnum(str, PyEnum):
    gram = "gram"
    kilogram = "kilogram"
    liter = "liter"
    milliliter = "mililiter"
    teaspoon = "teaspoon"
    tablespoon = "tablespoon"
    cup = "cup"
    piece = "piece"


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredientId = Column(
        Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    recipeId = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(DECIMAL(precision=10, scale=2), nullable=False)
    unit = Column(Enum(WeightUnitEnum), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    ingredient = relationship(
        "Ingredient", back_populates="recipe_ingredients", lazy="joined"
    )
    recipe_ing = relationship(
        "Recipes", back_populates="recipe_ingredients", lazy="joined"
    )
