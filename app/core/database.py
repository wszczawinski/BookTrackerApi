from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from .config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.SQL_ECHO,
    future=True,
)


@event.listens_for(SQLModel, "before_update", propagate=True)
def auto_update_timestamp(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = datetime.utcnow()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
