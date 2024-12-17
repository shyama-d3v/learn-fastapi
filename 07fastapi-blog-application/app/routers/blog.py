from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, database, auth
from loguru import logger


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    try:
        logger.info(f"User {current_user.id} is creating a new post.")

        return crud.create_post(db, post, str(current_user.id))
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Error creating post")


@router.get("/getallpost", response_model=schemas.PostListResponse)
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    try:
        if limit > 100:
            limit = 100
        logger.info(f"Fetching posts with skip={skip}, limit={limit}")
        posts = crud.get_posts(db, skip, limit)
        logger.info("......................", posts)
        response = {
            "success": True,
            "message": "Posts fetched successfully" if posts else "No posts found",
            "data": posts,
        }
        return response
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching posts",
        )


@router.get("/getpostById/{post_id}")
def get_post_by_id(post_id: str, db: Session = Depends(database.get_db)):
    try:
        logger.info(f"Fetching post with id={post_id}")
        post = crud.get_post_by_id(db, post_id)

        if post:
            return {
                "success": True,
                "message": "Post fetched successfully",
                "data": post,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching post",
        )


@router.put("/update-post")
def update_post(
    post_id: str,
    post: schemas.PostUpdate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    try:
        logger.info(f"User {current_user.id} is updating post {post_id}.")

        existing_post = crud.get_post_by_id(db, post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")

        updated_post = crud.update_post(db, post_id, post)

        response = {
            "success": True,
            "message": "Post updated successfully",
            "data": updated_post,
        }

        return response
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Error creating post")


@router.delete("/delete-post/{post_id}")
def delete_post(
    post_id: str,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    try:
        logger.info(f"User {current_user.id} is deleting post {post_id}.")

        existing_post = crud.get_post_by_id(db, post_id)
        if not existing_post:
            raise HTTPException(status_code=404, detail="Post not found")

        crud.delete_post(db, post_id)
        response = {"success": True, "message": "Post deleted successfully"}
        return response
    except Exception as e:
        logger.error(f"Error deleting post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting post")
