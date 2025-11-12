from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from app.core.exception_handlers import (
    generic_exception_handler,
    integrity_error_handler,
    operational_error_handler,
    sqlalchemy_error_handler,
)
from app.core.logging import setup_logging
from app.core.security_middleware import SecurityHeadersMiddleware

from .api.v1.router import api_router
from .core.api import api_metadata
from .core.config import settings
from .core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


setup_logging()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    lifespan=lifespan,
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
    if settings.ENVIRONMENT == "development"
    else None,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    openapi_tags=api_metadata["tags"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Database exception handlers
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(OperationalError, operational_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)

# Catch-all exception handler (must be last)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(SecurityHeadersMiddleware)

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
