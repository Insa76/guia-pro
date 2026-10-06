from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Guia Pro API"
    environment: str = "development"
    database_url: str = (
        "postgresql+psycopg://guia_pro:guia_pro@db:5432/guia_pro"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()