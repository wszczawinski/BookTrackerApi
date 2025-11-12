import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from app.core.config import settings

logger = logging.getLogger(__name__)


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handle database integrity constraint violations"""
    logger.warning(f"Database integrity error: {exc}")

    error_msg = str(exc.orig).lower() if exc.orig else str(exc).lower()

    if "unique" in error_msg or "duplicate" in error_msg:
        detail = "A resource with these values already exists"
    elif "foreign key" in error_msg:
        detail = "Referenced resource does not exist"
    elif "not null" in error_msg:
        detail = "Required field is missing"
    else:
        detail = "Database constraint violation"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": detail},
    )


async def operational_error_handler(
    request: Request, exc: OperationalError
) -> JSONResponse:
    """Handle database operational errors (connection issues, etc.)"""
    logger.error(f"Database operational error: {exc}", exc_info=True)

    if settings.ENVIRONMENT == "development":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "Database service temporarily unavailable",
                "error": str(exc),
            },
        )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Database service temporarily unavailable"},
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handle general SQLAlchemy errors"""
    logger.error(f"Database error: {exc}", exc_info=True)

    if settings.ENVIRONMENT == "development":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "A database error occurred",
                "error": str(exc),
                "type": type(exc).__name__,
            },
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A database error occurred"},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected exceptions"""
    logger.exception(f"Unhandled exception: {exc}")

    # In development, provide more details to help with debugging
    if settings.ENVIRONMENT == "development":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An internal server error occurred",
                "error": str(exc),
                "type": type(exc).__name__,
            },
        )

    # In production, hide implementation details
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred"},
    )
