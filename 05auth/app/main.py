from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from . import crud, models, schemas, security, database
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:8080",
]
# Create the tables in the database
models.Base.metadata.create_all(bind=database.engine)
app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


@app.get('/')
def entry_point():
    return "Welcome to the user management system"

# Register User
@app.post("/auth/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# Login User
@app.post("/auth/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = security.create_access_token(
        data={"sub": db_user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route: Get Current User
@app.get("/users/me", response_model=schemas.UserOut)
def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(security.decode_access_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    db_user = crud.get_user_by_username(db, token["sub"])
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
