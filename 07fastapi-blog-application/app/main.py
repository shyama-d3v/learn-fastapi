import os
from fastapi import FastAPI
from app.routers import user, blog
from app.database import Base, engine
from contextlib import asynccontextmanager
from loguru import logger
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Determine environment
ENVIRONMENT = os.getenv("ENVIRONMENT")
logger.info(f"ENVIRONMENT: {ENVIRONMENT}")
logger.add("app.log", rotation="1 MB", retention="7 days", level="INFO")


# Database cleanup function
async def shutdown():
    logger.info("Closing database connections...")


# Lifespan context manager for app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up and initializing database...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.success("Database initialized successfully.")
        yield
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise e
    finally:
        await shutdown()
        logger.info("App is shutting down...")


# Conditionally enable Swagger UI only in local environment
if ENVIRONMENT == "local":
    app = FastAPI(title="Blog Management API", version="1.0.0", lifespan=lifespan)
else:
    app = FastAPI(
        title="Blog Management API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
    )


# CORS Middleware for handling cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def entry_point():
    return {"message": "Welcome to the blog management system"}


app.include_router(user.router)
app.include_router(blog.router)
