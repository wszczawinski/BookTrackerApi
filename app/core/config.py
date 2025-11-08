from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field
from pydantic import PostgresDsn
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    ENVIRONMENT: str = "development"
    DEBUG: bool = Field(default=False)

    SERVER_HOST: str = Field(default="0.0.0.0")
    SERVER_PORT: int = Field(default=8000)
    SERVER_WORKERS_COUNT: int = Field(default=1)

    @property
    def SQL_ECHO(self) -> bool:
        return self.DEBUG and self.ENVIRONMENT == "development"

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Book Tracker API"

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_JWT_SECRET: str

    API_JWT_SECRET: str
    API_JWT_ALGORITHM: str
    API_JWT_EXPIRE_HOURS: int
    API_JWT_ISSUER: str
    API_JWT_COOKIE_NAME: str

    CORS_ORIGINS: list[str]
    CORS_ALLOW_CREDENTIALS: bool
    CORS_ALLOW_METHODS: list[str]
    CORS_ALLOW_HEADERS: list[str]

    TRUSTED_HOSTS: list[str]


settings = Settings()  # type: ignore
