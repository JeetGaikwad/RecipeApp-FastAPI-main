from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey, func
from config.db_config import Base


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipeId = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    visibility = Column(
        Enum("public", "private", name="visiblityenum"),
        nullable=False,
        server_default="private",
    )
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )
