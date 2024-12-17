from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import schemas, models, crud, auth, database
import logging

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

logger = logging.getLogger(__name__)


@router.post(
    "/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        logger.warning(
            f"Attempt to register with already registered email: {user.email}"
        )
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)
    user.password = hashed_password
    created_user = crud.create_user(db, user)
    logger.info(f"User registered successfully: {user.email}")
    return created_user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        logger.warning(f"Failed login attempt for email: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
def get_current_user_data(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user
