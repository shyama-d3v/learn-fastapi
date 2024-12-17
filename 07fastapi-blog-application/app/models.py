from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255))
    content = Column(String(255))
    published = Column(Boolean, default=False)
    created_at = Column(
        String(255), default=lambda: datetime.now(timezone.utc).isoformat()
    )
    owner_id = Column(CHAR(36), ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
