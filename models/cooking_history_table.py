from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db_config import Base


class CookingHistory(Base):
    __tablename__ = "cooking_historys"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipeId = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    # Define relationships
    user = relationship("Users", back_populates="cooking_historys", lazy="joined")
    recipe = relationship("Recipes", back_populates="cooking_historys", lazy="joined")
