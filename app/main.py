from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
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

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(api_router, prefix=settings.API_V1_STR)
