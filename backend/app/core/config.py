from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "Insurance Claims & Policy Intelligence Assistant"
    API_V1_STR: str = "/api/v1"

    # Host & Ports
    HOST_BACKEND_PORT: int = 8005
    HOST_FRONTEND_PORT: int = 3000

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8005",
    ]

    # Security & Auth
    SECRET_KEY: str = Field(
        default="supersecretjwtkeychangeinproductionminimum32characterslong",
        description="JWT secret key for signing tokens",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    # Fernet Encryption Key (at rest for provider secrets)
    # Default 32-byte url-safe base64 key
    ENCRYPTION_KEY: str = Field(
        default="D7MvZ8q7X8zBqG2WjX8_4T7fN_3kY9pQ5mR1sT3vW4Y=",
        description="Fernet key for encrypting provider keys at rest",
    )

    # Seed Admin User
    INITIAL_ADMIN_EMAIL: str = "admin@insurance.internal"
    INITIAL_ADMIN_PASSWORD: str = "AdminSecurePass123!"
    INITIAL_ADMIN_NAME: str = "System Administrator"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "insurance_genai"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5435
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5435/insurance_genai"
    )

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6381
    REDIS_PASSWORD: str = ""
    REDIS_URL: str = Field(default="redis://localhost:6381/0")

    # Storage
    STORAGE_TYPE: str = "local"
    STORAGE_LOCAL_PATH: str = "./storage"
    MAX_UPLOAD_SIZE_MB: int = 25

    # Rate Limiting
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 10
    CHAT_RATE_LIMIT_PER_MINUTE: int = 60

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
