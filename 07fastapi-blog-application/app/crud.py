from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from loguru import logger


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username, email=user.email, password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_post(db: Session, post: schemas.PostCreate, user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        logger.warning(f"User with ID {user_id} does not exist.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_post = models.Post(title=post.title, content=post.content, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: str, post_update: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    update_data = {}
    if post_update.title is not None:
        update_data["title"] = post_update.title
    if post_update.content is not None:
        update_data["content"] = post_update.content
    if post_update.published is not None:
        update_data["published"] = post_update.published

    db.query(models.Post).filter(models.Post.id == post_id).update(update_data)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post_by_id(db: Session, post_id: str):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Post)
        .filter(models.Post.published == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_post(db: Session, post_id: str):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return post
