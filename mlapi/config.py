from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ASSEMBLY_API_KEY: str
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(env_file=".env")
