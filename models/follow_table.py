from sqlalchemy import Column, Integer, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from config.db_config import Base


class Follows(Base):
    __tablename__ = "follows"

    followerId = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    followeeId = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    createdAt = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (PrimaryKeyConstraint("followerId", "followeeId"),)
