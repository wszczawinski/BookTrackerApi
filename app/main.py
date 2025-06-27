from fastapi import FastAPI

from contextlib import asynccontextmanager

from .core.config import settings
from .core.api import api_metadata
from .core.database import init_db, drop_db_and_tables
from .api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # drop_db_and_tables()
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=api_metadata["tags"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
