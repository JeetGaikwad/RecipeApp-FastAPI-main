from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db_config import Base


class ForkedRecipe(Base):
    __tablename__ = "forked_recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipeId = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    recipeName = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    recipeType = Column(Enum("veg", "nonveg", name="tag"), nullable=False)
    peopleCount = Column(Integer, nullable=False, server_default="1")
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    user = relationship("Users", back_populates="forked_recipes", lazy="joined")
    recipe = relationship("Recipes", back_populates="forked_recipes", lazy="joined")
