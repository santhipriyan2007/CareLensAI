from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CareLens AI API"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()