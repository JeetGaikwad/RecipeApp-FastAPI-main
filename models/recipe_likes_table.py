from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db_config import Base


class RecipeLike(Base):
    __tablename__ = "recipe_likes"

    userId = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    recipeId = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    # Use string-based references to avoid initialization errors
    user = relationship("Users", back_populates="recipe_likes", lazy="joined")
    recipe = relationship("Recipes", back_populates="likes", lazy="joined")
