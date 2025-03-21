from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from config.db_config import Base


class RecipeComment(Base):
    __tablename__ = "recipe_comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipeId = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    parentCommentId = Column(
        Integer, ForeignKey("recipe_comments.id", ondelete="CASCADE"), nullable=True
    )
    comment = Column(Text, nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("Users", back_populates="comments", lazy="joined")
    recipe = relationship("Recipes", back_populates="comments", lazy="joined")

    parent_comment = relationship(
        "RecipeComment",
        remote_side=[id],
        backref="replies",
    )
