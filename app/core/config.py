from pydantic_settings import BaseSettings # type: ignore
class Settings(BaseSettings):
    APP_NAME: str = "Banking API"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

print(settings.DATABASE_URL)