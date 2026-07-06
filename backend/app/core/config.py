from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   
    # Application
    APP_NAME: str
    APP_VERSION: str

    # Database
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # OCR
    TESSERACT_CMD: str
    POPPLER_PATH: str

    # Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()