from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routes.todo import router as todo_router
from .routes.user import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    init_db()
    yield
    # Cleanup or shutdown logic can be added here if needed


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Include routers for the application
    app.include_router(todo_router, tags=["todos"])
    app.include_router(auth_router, prefix="/auth", tags=["todos"])

    return app


# Create the app instance
app = create_app()
