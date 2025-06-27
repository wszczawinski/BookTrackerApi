from sqlmodel import Session, SQLModel, create_engine

from .config import settings

engine = create_engine(
    str(settings.DATABASE_URL),
    echo=settings.SQL_ECHO,
)


def init_db():
    SQLModel.metadata.create_all(engine)


# TODO: remove and use alembic for migrations after initial development
def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
