from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    debug: bool = False
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str
    jwt_validity: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
