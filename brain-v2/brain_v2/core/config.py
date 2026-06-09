from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "NESLA Brain V2"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Central intelligence service for the NESLA ecosystem."
    DATABASE_URL: str = "postgresql+asyncpg://nesla:nesla_change_me@postgres:5432/nesla_brain_v2"
    KNOWLEDGE_SOURCE_DIR: str = "./knowledge_base"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()