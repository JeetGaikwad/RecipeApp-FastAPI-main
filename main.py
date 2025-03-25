# Loading the .env file
from dotenv import load_dotenv
from os.path import join, dirname
from helper.api_helper import APIHelper
from helper.cors_helper import CORSHelper
from helper.logger_helper import setup_logger

# Setting up dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Importing libraries
from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from contextlib import asynccontextmanager
from routes.auth import auth
from routes.users import user
from routes.recipes import recipe
from routes.forked_recipes import forked_recipe
from routes.recipe_ingredients import ingredient
from routes.comments import recipe_comment
from routes.cooking_historys import cooking_history
from routes.wishlists import wishlist
from routes.admins import admin
from fastapi.exceptions import RequestValidationError
import i18n
import os

# Database Connection Setup
DATABASE_URL = f"mysql+aiomysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_URL')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Setup Logger
setup_logger()

# Setup i18n
i18n.load_path.append("language/")
i18n.set("filename_format", "{namespace}.{locale}.{format}")
i18n.set("file_format", "json")


# Lifespan Function for Startup and Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Starting up RecipeApp...")

    # 1️⃣ Test Database Connection
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda conn: conn.execute(text("SELECT 1")))
        print("✅ Database connected successfully.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    yield  # ⏳ The app runs here

    # 3️⃣ Cleanup Resources on Shutdown
    print("🛑 Shutting down RecipeApp...")
    await engine.dispose()


# Initializing FastAPI with Lifespan
app = FastAPI(
    title="RecipeApp-FastAPI",
    version="0.0.1",
    lifespan=lifespan,  # ✅ Adding lifespan here
)

# Setup CORS
CORSHelper.setup_cors(app)


# Request validation error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if exc.errors()[0]["type"] == "value_error":
        return APIHelper.send_error_response(
            errorMessageKey=f"{exc.errors()[0]['msg']}"
        )
    else:
        return APIHelper.send_error_response(
            errorMessageKey=f"{exc.errors()[0]['loc'][1]} {exc.errors()[0]['msg']}"
        )


# Including the routes
app.include_router(auth)
app.include_router(user)
app.include_router(recipe)
app.include_router(forked_recipe)
app.include_router(ingredient)
app.include_router(recipe_comment)
app.include_router(cooking_history)
app.include_router(wishlist)
app.include_router(admin)
