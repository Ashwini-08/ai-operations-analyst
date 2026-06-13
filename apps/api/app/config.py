from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Operations Analyst API"
    app_version: str = "0.1.0"
    environment: str = "local"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ai_ops"

    class Config:
        env_file = ".env"


settings = Settings()