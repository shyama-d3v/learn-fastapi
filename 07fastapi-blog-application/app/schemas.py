from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime, timezone


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    created_at: datetime = datetime.now(timezone.utc)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class Post(PostBase):
    id: uuid.UUID
    owner_id: uuid.UUID

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    success: bool
    message: str
    data: List[Post]

    class Config:
        from_attributes = True
